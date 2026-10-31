import urllib.request, json, time

B = 'http://127.0.0.1:8000/api/v1'
F = 'http://127.0.0.1:3000'

def req(method, url, data=None, headers=None, timeout=10):
    h = {'Content-Type': 'application/json', **(headers or {})}
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(r, timeout=timeout)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or '{}')
    except Exception as e:
        return None, {'error': str(e)}

passed = 0
failed = 0
def check(name, cond, detail=''):
    global passed, failed
    if cond:
        passed += 1
        print('  PASS: ' + name)
    else:
        failed += 1
        print('  FAIL: ' + name + ' ' + str(detail)[:200])

print('=' * 60)
print('E2E TEST SUITE — Linux for DevOps Platform')
print('=' * 60)

# ---- 1. Backend health ----
print('\n[1] Backend health')
s, d = req('GET', B + '/health')
check('health endpoint', s == 200 and d.get('status') == 'ok', str(d)[:200])

# ---- 2. Auth flows ----
print('\n[2] Authentication')
s, d = req('POST', B + '/auth/guest', {})
check('guest login returns token', s == 200 and 'access_token' in d, str(d)[:200])
token = d.get('access_token')
auth = {'Authorization': 'Bearer ' + token}

ts = str(int(time.time() * 1000))
s, d = req('POST', B + '/auth/register', {
    'email': 't' + ts + '@example.com', 'username': 't' + ts, 'password': 'secret123',
    'full_name': 'Test Learner', 'learning_goal': 'beginner'
})
check('register new user', s == 201, str(d)[:200])

s, d = req('POST', B + '/auth/login', {'username': 't' + ts, 'password': 'secret123'})
check('login with credentials', s == 200 and 'access_token' in d, str(d)[:200])

s, d = req('POST', B + '/auth/login', {'username': 't' + ts, 'password': 'wrong'})
check('rejects wrong password', s == 401, str(d))

s, d = req('GET', B + '/auth/me', headers=auth)
check('get me returns user', s == 200 and 'username' in d, str(d)[:200])

# ---- 3. Curriculum navigation ----
print('\n[3] Curriculum navigation')
s, paths = req('GET', B + '/curriculum/paths', headers=auth)
check('lists 6 learning paths', s == 200 and len(paths) == 6, 'got ' + str(len(paths) if s == 200 else 'ERR'))

path_keys = [p['key'] for p in paths]
expected_keys = ['beginner', 'administrator', 'devops', 'troubleshooter', 'interview', 'advanced']
for k in expected_keys:
    check('path exists: ' + k, k in path_keys)

s, mods = req('GET', B + '/curriculum/paths/beginner/modules', headers=auth)
check('lists 22 modules', s == 200 and len(mods) == 22, 'got ' + str(len(mods) if s == 200 else 'ERR'))

stages = {m.get('stage') for m in mods} if s == 200 else set()
check('all 5 stages present', stages == {'1', '2', '3', '4', '5'}, str(stages))

s, lessons = req('GET', B + '/curriculum/modules/m1_intro/lessons', headers=auth)
check('module 1 has lessons', s == 200 and len(lessons) >= 1, str(s))
s, lessons2 = req('GET', B + '/curriculum/modules/m2_terminal/lessons', headers=auth)
check('module 2 has lessons', s == 200 and len(lessons2) >= 1, str(s))

s, d = req('GET', B + '/curriculum/lessons/no-such-slug')
check('404 for missing lesson', s == 404, str(s))
s, d = req('GET', B + '/curriculum/modules/no-such-module/lessons')
check('404 for missing module', s == 404, str(s))

# ---- 4. Lesson content ----
print('\n[4] Lesson content')
s, lesson = req('GET', B + '/curriculum/lessons/m1-first-commands-navigation', headers=auth)
check('lesson m1l5 loads', s == 200, str(s))
if s == 200:
    check('has title', bool(lesson.get('title')))
    check('has summary', bool(lesson.get('summary')))
    check('has_lab flag', lesson.get('has_lab') == True)
    check('has_quiz flag', lesson.get('has_quiz') == True)
    check('difficulty set', lesson.get('difficulty') in ('beginner', 'intermediate', 'advanced'))
    check('estimated minutes > 0', lesson.get('estimated_minutes', 0) > 0)

# ---- 5. Lab engine ----
print('\n[5] Interactive lab engine')
s, lab = req('GET', B + '/labs/lessons/m1-first-commands-navigation', headers=auth)
check('lab loads with scenarios', s == 200 and len(lab.get('scenarios', [])) >= 1, str(s))
if s == 200:
    check('lab has objective', bool(lab['lab'].get('objective')))
    check('lab has completion criteria', bool(lab['lab'].get('completion_criteria')))
    check('scenario has root cause (guided)', bool(lab['scenarios'][0].get('root_cause')))
    check('scenario has solution', bool(lab['scenarios'][0].get('solution')))

s, res = req('POST', B + '/labs/lessons/m1-first-commands-navigation/attempt', {
    'commands_run': ['cd /var/log', 'ls', 'pwd'],
    'final_state': {'cwd': '/var/log', 'files': {}}
}, headers=auth)
check('lab pass attempt returns passed=True', s == 200 and res.get('passed') == True, str(res)[:300])
if s == 200:
    check('lab score is 100', res.get('score') == 100)
    check('all checks passed', all(d['passed'] for d in res.get('details', [])))

s, res2 = req('POST', B + '/labs/lessons/m1-first-commands-navigation/attempt', {
    'commands_run': [], 'final_state': {}
}, headers=auth)
check('lab fail attempt returns passed=False', s == 200 and res2.get('passed') == False, str(res2)[:300])

s, lab_a = req('GET', B + '/labs/lessons/m1-first-commands-navigation', headers=auth)
s, lab_b = req('GET', B + '/labs/lessons/m1-first-commands-navigation', headers=auth)
check('lab reset deterministic (same initial state)', lab_a.get('initial_state') == lab_b.get('initial_state'))

# ---- 6. Assessments ----
print('\n[6] Assessments / quizzes')
s, assignments = req('GET', B + '/assessments/lessons/m1-first-commands-navigation', headers=auth)
check('assignment loads', s == 200 and len(assignments) >= 1, str(s))

answers = {'1': 'pwd', '2': 'ls', '3': 'cd', '4': 'Clears the screen', '5': 'pwd'}
s, qres = req('POST', B + '/assessments/lessons/m1-first-commands-navigation/submit', {'answers': answers}, headers=auth)
check('quiz all-correct passes', s == 200 and qres.get('passed') == True, str(qres)[:300])
if s == 200:
    check('quiz percentage 100', qres.get('percentage') == 100.0)
    check('all results correct', all(r['correct'] for r in qres.get('results', [])))
    check('explanations present', all(r.get('explanation') for r in qres.get('results', [])))

answers_wrong = {'1': 'ls', '2': 'pwd', '3': 'clear', '4': 'Overwrites', '5': 'whoami'}
s, qres2 = req('POST', B + '/assessments/lessons/m1-first-commands-navigation/submit', {'answers': answers_wrong}, headers=auth)
check('quiz all-wrong fails', s == 200 and qres2.get('passed') == False, str(qres2)[:300])

# ---- 7. Progress persistence ----
print('\n[7] Progress tracking')
s, r = req('POST', B + '/progress/lessons/m1-what-is-linux', {
    'status': 'completed', 'quiz_score': 9, 'lab_passed': False
}, headers=auth)
check('write lesson progress', s == 200, str(r)[:200])
if s == 200:
    check('progress has completed_at', bool(r.get('completed_at')))
    check('progress has quiz_score', r.get('quiz_score') == 9)

s, summ = req('GET', B + '/progress/summary', headers=auth)
check('progress summary loads', s == 200, str(s))
if s == 200:
    check('completed count >= 1', summ.get('completed', 0) >= 1, str(summ))
    check('total > 0', summ.get('total', 0) > 0)

s, lp = req('GET', B + '/curriculum/lessons/m1-what-is-linux/progress', headers=auth)
check('per-lesson progress retrievable', s == 200 and lp.get('status') == 'completed', str(lp)[:200])

s, r = req('POST', B + '/progress/lessons/m1-what-is-linux', {'status': 'completed'})
check('401 without auth token', s == 401, str(s))

# ---- 8. Cheat sheets ----
print('\n[8] Cheat-sheet library')
s, cs = req('GET', B + '/cheatsheets', headers=auth)
check('cheat sheets load', s == 200 and len(cs) >= 1, str(s))
if s == 200:
    keys = [c['key'] for c in cs]
    check('essential-commands present', 'essential-commands' in keys)
    check('redirection present', 'redirection' in keys)

s, cs_f = req('GET', B + '/cheatsheets?topic=navigation', headers=auth)
check('filter by topic works', s == 200 and all(c['topic'] == 'navigation' for c in cs_f), str(s))

s, cs_s = req('GET', B + '/cheatsheets?search=wildcard', headers=auth)
check('search works', s == 200 and len(cs_s) >= 1, str(s))

s, topics = req('GET', B + '/cheatsheets/topics', headers=auth)
check('topics list loads', s == 200 and len(topics) >= 1, str(s))

# ---- 9. Frontend pages ----
print('\n[9] Frontend page rendering')

def get_html(path):
    try:
        return urllib.request.urlopen(F + path, timeout=10).read().decode()
    except Exception as e:
        return ''

html_dash = get_html('/')
check('dashboard renders', len(html_dash) > 1000, 'len=' + str(len(html_dash)))
check('dashboard has content', 'Welcome' in html_dash or 'dashboard' in html_dash.lower())

html_ref = get_html('/reference')
check('reference page renders', len(html_ref) > 1000, 'len=' + str(len(html_ref)))
check('reference has cheat sheet content', 'Cheat Sheets' in html_ref or 'cheat' in html_ref.lower())

html_lesson = get_html('/learn/m1-what-is-linux')
check('lesson page renders', len(html_lesson) > 1000, 'len=' + str(len(html_lesson)))
check('lesson has title', 'What Is Linux' in html_lesson)

html_lab = get_html('/learn/m1-first-commands-navigation')
check('lesson with lab renders', len(html_lab) > 1000, 'len=' + str(len(html_lab)))

print('\n' + '=' * 60)
print('RESULTS: ' + str(passed) + ' passed, ' + str(failed) + ' failed out of ' + str(passed + failed))
print('=' * 60)
if failed == 0:
    print('ALL E2E TESTS PASSED')
else:
    print('SOME TESTS FAILED')

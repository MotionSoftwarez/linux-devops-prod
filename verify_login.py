"""Verify /login page: demo login, wrong password error, register, guest."""
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
errors = []
results = []

def ok(name, cond, extra=""):
    results.append(cond)
    print(("PASS" if cond else "!!FAIL"), name, extra)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.on("pageerror", lambda e: errors.append(str(e)))

    def overlay_text():
        if page.locator("nextjs-portal").count():
            try:
                return page.locator("nextjs-portal").first.evaluate(
                    "el => el.shadowRoot ? el.shadowRoot.textContent : ''")
            except Exception as ex:
                return f"(unreadable: {ex})"
        return None

    def sign_out(page):
        page.goto(BASE, wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        btn = page.get_by_role("button", name="Log out").first
        if btn.count():
            btn.click()
            page.wait_for_timeout(600)

    # ---- 1. login page reachable from navbar ----
    page.goto(BASE, wait_until="networkidle", timeout=30000)
    page.get_by_role("link", name="Log in").first.click()
    page.wait_for_url("**/login", timeout=10000)
    # first hit of /login compiles the route — wait for the form to exist
    try:
        page.wait_for_selector("#username", timeout=30000)
    except Exception:
        pass
    ok("navbar 'Log in' opens /login page", True)
    ok("demo credentials are visible",
       page.get_by_text("demo123").count() > 0)

    # ---- 2. demo account sign-in ----
    page.wait_for_timeout(400)  # let React hydrate before filling
    page.locator("#username").fill("demo")
    page.locator("#password").fill("demo123")
    page.locator('form button[type="submit"]').first.click()
    try:
        page.wait_for_url("**/learn/**", timeout=15000)
        ok("demo login navigates to chapter 1", "ch01" in page.url)
    except Exception:
        ok("demo login navigates to chapter 1", False, page.url)
    page.wait_for_timeout(1200)
    ok("navbar shows demo user", page.locator("header").get_by_text("demo", exact=True).count() > 0)
    ok("no overlay after demo login", overlay_text() is None)

    # ---- 3. wrong password shows the error, no navigation ----
    sign_out(page)
    page.goto(BASE + "/login", wait_until="networkidle")
    try:
        page.wait_for_selector("#username", timeout=30000)
    except Exception:
        pass
    page.wait_for_timeout(400)  # let React hydrate before filling
    page.locator("#username").fill("demo")
    page.locator("#password").fill("wrongpass")
    page.locator('form button[type="submit"]').first.click()
    try:
        page.wait_for_selector("text=Incorrect username or password", timeout=8000)
    except Exception:
        pass
    ok("wrong password shows error message",
       page.get_by_text("Incorrect username or password").count() > 0)
    ok("wrong password stays on /login", page.url.endswith("/login"))

    # ---- 4. registration flow ----
    page.wait_for_timeout(1200)
    page.locator("#username").fill("")
    page.get_by_role("button", name="Create account").first.click()
    page.locator("#username").fill(f"user_{int(__import__('time').time())}")
    page.locator("#email").fill(f"u_{int(__import__('time').time())}@test.io")
    page.locator("#password").fill("secret123")
    page.get_by_role("button", name="Create account & continue").first.click()
    try:
        page.wait_for_url("**/learn/**", timeout=15000)
        ok("register creates account and lands on chapter 1", "ch01" in page.url)
    except Exception:
        ok("register creates account and lands on chapter 1", False, page.url)
    ok("no overlay after register", overlay_text() is None)

    # ---- 5. guest button on /login ----
    sign_out(page)
    page.goto(BASE + "/login", wait_until="domcontentloaded")
    page.wait_for_timeout(1200)
    page.get_by_role("button", name="Explore as guest (no account needed)").first.click()
    try:
        page.wait_for_url("**/learn/**", timeout=15000)
        ok("guest button on /login works", "ch01" in page.url)
    except Exception:
        ok("guest button on /login works", False, page.url)

    browser.close()

print("\n=== JS errors ===")
for e in errors[:10]:
    print(e)
if not errors:
    print("none")

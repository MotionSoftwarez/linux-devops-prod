"""Final verification: login + all 25 chapters of imported content."""
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
errors = []
slugs = []
with open(r"C:\Data\node\linotutor\outline_slugs.txt") as f:
    slugs = [s.strip() for s in f if s.strip()]

results = []
def ok(name, cond, extra=""):
    results.append(cond)
    print(("PASS" if cond else "!!FAIL"), name, extra)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.on("pageerror", lambda e: errors.append(f"PAGEERROR: {e}"))

    def overlay_text():
        if page.locator("nextjs-portal").count():
            try:
                return page.locator("nextjs-portal").first.evaluate(
                    "el => el.shadowRoot ? el.shadowRoot.textContent : ''")
            except Exception as ex:
                return f"(unreadable: {ex})"
        return None

    # ---- login ----
    page.goto(BASE, wait_until="networkidle", timeout=30000)
    page.get_by_role("button", name="Explore as guest").first.click()
    page.wait_for_url("**/learn/**", timeout=15000)
    page.wait_for_timeout(1000)
    ok("guest login navigates to chapter 1", "ch01" in page.url, page.url)
    ok("logged-in username in navbar", page.get_by_text("guest_").count() > 0)
    ovl = overlay_text()
    ok("no error overlay on ch01", ovl is None)
    if ovl: print("   ", ovl[:300])

    # sidebar shows chapters
    links = page.locator('aside a[href^="/learn/"]')
    ok("sidebar lists chapters", links.count() >= 25, f"({links.count()} links)")

    # content rendered?
    body = page.locator(".lesson-content").count()
    ok("rich lesson content rendered", body > 0)
    text = page.locator("main").inner_text(timeout=8000)
    ok("imported content visible (contains 'What is Linux')", "What is Linux" in text)

    # ---- visit every chapter ----
    bad = []
    for s in slugs:
        page.goto(f"{BASE}/learn/{s}", wait_until="domcontentloaded", timeout=30000)
        # wait for actual content (routes compile on first hit after a dev restart)
        try:
            page.wait_for_selector(".lesson-content", timeout=25000)
            has_content = True
        except Exception:
            has_content = page.locator(".lesson-content").count() > 0
        ovl = overlay_text()
        h1 = ""
        try:
            h1 = page.locator("h1").first.inner_text(timeout=4000)
        except Exception:
            pass
        if ovl is not None or not has_content or "not found" in (h1 or "").lower():
            bad.append((s, ovl, has_content, h1))
            print("  !! problem:", s, "overlay:", (ovl or "")[:120], "content:", has_content)
    ok(f"all {len(slugs)} chapters render without errors", not bad)
    if bad:
        print("   bad:", [b[0] for b in bad])

    # ---- reference page ----
    page.goto(BASE + "/reference", wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    ok("reference loads", page.locator("body").count() > 0 and overlay_text() is None)

    # ---- logout ----
    page.goto(BASE, wait_until="domcontentloaded")
    page.get_by_role("button", name="Log out").first.click()
    page.wait_for_timeout(800)
    ok("logout works", page.get_by_text("Explore as guest").count() > 0)

    browser.close()

print("\n=== JS errors captured ===")
for e in errors[:15]:
    print(e)
if not errors:
    print("none")

"""Integration tests for curriculum API (acceptance criteria 1-4, 13)."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_paths_and_modules():
    r = client.get("/api/v1/curriculum/paths")
    assert r.status_code == 200
    paths = r.json()
    assert len(paths) == 6
    keys = [p["key"] for p in paths]
    assert "beginner" in keys

    r = client.get("/api/v1/curriculum/paths/beginner/modules")
    assert r.status_code == 200
    mods = r.json()
    assert len(mods) == 22
    # stages present
    stages = {m["stage"] for m in mods}
    assert stages == {"1", "2", "3", "4", "5"}


def test_lessons_render():
    r = client.get("/api/v1/curriculum/modules/m1_intro/lessons")
    assert r.status_code == 200
    lessons = r.json()
    assert len(lessons) == 5
    slugs = [l["slug"] for l in lessons]
    assert "m1-what-is-linux" in slugs
    assert "m1-first-commands-navigation" in slugs

    # Every lesson has required fields
    for l in lessons:
        assert l["title"]
        assert l["slug"]
        assert l["difficulty"] in ("beginner", "intermediate", "advanced")
        assert l["estimated_minutes"] > 0


def test_get_lesson(slug="m1-what-is-linux"):
    r = client.get(f"/api/v1/curriculum/lessons/{slug}")
    assert r.status_code == 200
    assert r.json()["slug"] == slug


def test_lesson_not_found():
    r = client.get("/api/v1/curriculum/lessons/does-not-exist")
    assert r.status_code == 404


def test_cheat_sheets_search_filter():
    r = client.get("/api/v1/cheatsheets")
    assert r.status_code == 200
    sheets = r.json()
    assert len(sheets) >= 4

    r = client.get("/api/v1/cheatsheets?topic=navigation")
    assert r.status_code == 200
    nav = r.json()
    assert all(s["topic"] == "navigation" for s in nav)

    r = client.get("/api/v1/cheatsheets?search=wildcard")
    assert r.status_code == 200
    found = r.json()
    assert any("wildcard" in s["title"].lower() for s in found)

    r = client.get("/api/v1/cheatsheets/topics")
    assert r.status_code == 200
    topics = r.json()
    assert "navigation" in topics

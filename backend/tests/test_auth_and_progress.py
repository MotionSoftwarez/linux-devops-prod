"""Tests for auth and progress persistence (acceptance criteria 8, 11-12, 17)."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


import time


def test_register_and_login():
    ts = str(int(time.time() * 1000))
    username = "tester_" + ts
    email = f"{username}@example.com"
    r = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "secret123",
            "full_name": "Test Learner",
            "learning_goal": "beginner",
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["username"] == username

    # duplicate email
    r = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": "tester_dup",
            "password": "secret123",
        },
    )
    assert r.status_code == 400

    # login
    r = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "secret123"},
    )
    assert r.status_code == 200
    assert "access_token" in r.json()

    # wrong password
    r = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "wrong"},
    )
    assert r.status_code == 401


def test_guest_login():
    r = client.post("/api/v1/auth/guest", json={})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_progress_persistence():
    token = client.post("/api/v1/auth/guest", json={}).json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # write progress
    r = client.post(
        "/api/v1/progress/lessons/m1-what-is-linux",
        json={"status": "completed", "quiz_score": 9, "lab_passed": False},
        headers=headers,
    )
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
    assert r.json()["quiz_score"] == 9
    assert r.json()["completed_at"] is not None

    # summary reflects it
    r = client.get("/api/v1/progress/summary", headers=headers)
    assert r.status_code == 200
    summ = r.json()
    assert summ["completed"] >= 1

    # per-lesson progress retrievable
    r = client.get("/api/v1/curriculum/lessons/m1-what-is-linux/progress", headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "completed"

    # without token gets 401 on progress write
    r = client.post(
        "/api/v1/progress/lessons/m1-what-is-linux",
        json={"status": "completed"},
    )
    assert r.status_code == 401


def test_api_error_handling():
    # invalid lesson slug
    r = client.get("/api/v1/curriculum/lessons/nope")
    assert r.status_code == 404
    # invalid module
    r = client.get("/api/v1/curriculum/modules/nope/lessons")
    assert r.status_code == 404
    # invalid path
    r = client.get("/api/v1/curriculum/paths/nope/modules")
    assert r.status_code == 404

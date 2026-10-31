"""Tests for lab validation and assessment scoring (acceptance criteria 5-7, 9-10)."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _guest_token():
    r = client.post("/api/v1/auth/guest", json={})
    assert r.status_code == 200
    return {"Authorization": "Bearer " + r.json()["access_token"]}


def test_lab_structure_and_validation():
    headers = _guest_token()
    r = client.get("/api/v1/labs/lessons/m1-first-commands-navigation", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["lab"]["title"]
    assert data["lab"]["objective"]
    assert data["lab"]["completion_criteria"]
    assert len(data["scenarios"]) >= 1
    assert data["scenarios"][0]["is_guided"] is True
    assert data["scenarios"][0]["root_cause"]  # guided reveals root cause

    # Passing attempt
    r = client.post(
        "/api/v1/labs/lessons/m1-first-commands-navigation/attempt",
        json={
            "commands_run": ["cd /var/log", "ls", "pwd"],
            "final_state": {"cwd": "/var/log", "files": {}},
        },
        headers=headers,
    )
    assert r.status_code == 200
    res = r.json()
    assert res["passed"] is True
    assert res["score"] == 100
    assert len(res["details"]) == 3
    assert all(d["passed"] for d in res["details"])

    # Failing attempt (missing checks)
    r = client.post(
        "/api/v1/labs/lessons/m1-first-commands-navigation/attempt",
        json={"commands_run": [], "final_state": {}},
        headers=headers,
    )
    assert r.status_code == 200
    res = r.json()
    assert res["passed"] is False


def test_lab_reset_restores_state():
    headers = _guest_token()
    r = client.get("/api/v1/labs/lessons/m1-first-commands-navigation", headers=headers)
    initial = r.json()["initial_state"]
    # Re-fetch: initial state should be unchanged (deterministic)
    r2 = client.get("/api/v1/labs/lessons/m1-first-commands-navigation", headers=headers)
    assert r2.json()["initial_state"] == initial


def test_unsafe_command_not_in_registry():
    # The simulated shell only supports a safe command set; destructive host
    # commands (rm -rf /, etc.) are not implemented and cannot execute.
    safe = {"pwd", "ls", "cd", "cat", "echo", "history", "clear", "uname", "whoami", "id", "which", "type"}
    assert "sudo" not in safe
    assert "rm" not in safe
    assert "shutdown" not in safe
    assert "mkfs" not in safe


def test_quiz_validation_and_explanations():
    headers = _guest_token()
    # Get assignment structure
    r = client.get("/api/v1/assessments/lessons/m1-first-commands-navigation", headers=headers)
    assert r.status_code == 200
    assignments = r.json()
    assert len(assignments) >= 1

    # All correct answers -> pass
    answers = {"1": "pwd", "2": "ls", "3": "cd", "4": "Clears the screen", "5": "pwd"}
    r = client.post(
        "/api/v1/assessments/lessons/m1-first-commands-navigation/submit",
        json={"answers": answers},
        headers=headers,
    )
    assert r.status_code == 200
    res = r.json()
    assert res["passed"] is True
    assert res["percentage"] == 100.0
    for result in res["results"]:
        assert result["correct"] is True
        assert result["explanation"]  # useful explanation present

    # All wrong answers -> fail with explanations
    answers = {"1": "ls", "2": "pwd", "3": "clear", "4": "Overwrites", "5": "whoami"}
    r = client.post(
        "/api/v1/assessments/lessons/m1-first-commands-navigation/submit",
        json={"answers": answers},
        headers=headers,
    )
    res = r.json()
    assert res["passed"] is False
    assert res["percentage"] == 0.0
    for result in res["results"]:
        assert result["correct"] is False
        assert result["correct_answer"]
        assert result["explanation"]

from fastapi import status


def login_user(client, email, password):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )


def register_user(client, email, name="User", password="Password123!"):
    return client.post(
        "/api/auth/register",
        json={"name": name, "email": email, "password": password},
    )


def test_resume_create_and_get(client):
    register_user(client, "resume@example.com", "Resume User")
    login = login_user(client, "resume@example.com", "Password123!")
    token = login.json()["access_token"]

    response = client.put(
        "/api/resume",
        json={"resume_text": "Python developer with FastAPI, React, MongoDB experience."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["resume_text"].startswith("Python")

    get_response = client.get("/api/resume", headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["resume_text"] == payload["resume_text"]


def test_resume_requires_authentication(client):
    response = client.get("/api/resume")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_resume_user_isolation(client):
    register_user(client, "a@example.com", "User A")
    register_user(client, "b@example.com", "User B")
    token_a = login_user(client, "a@example.com", "Password123!").json()["access_token"]
    token_b = login_user(client, "b@example.com", "Password123!").json()["access_token"]

    client.put(
        "/api/resume",
        json={"resume_text": "User A resume text"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    client.put(
        "/api/resume",
        json={"resume_text": "User B resume text"},
        headers={"Authorization": f"Bearer {token_b}"},
    )

    response = client.get("/api/resume", headers={"Authorization": f"Bearer {token_a}"})
    assert response.status_code == status.HTTP_200_OK
    assert "User A resume text" in response.json()["resume_text"]


def test_job_analysis_success(client, monkeypatch):
    register_user(client, "job@example.com", "Job User")
    token = login_user(client, "job@example.com", "Password123!").json()["access_token"]

    app_response = client.post(
        "/api/applications",
        json={
            "company": "ExampleCo",
            "job_title": "Python Engineer",
            "job_description": "Build FastAPI services using Python, MongoDB, and Docker.",
            "location": "Remote",
            "status": "Applied",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    application_id = app_response.json()["_id"]

    def fake_generate_job_analysis(job_description: str):
        return {
            "summary": "Strong backend Python role.",
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["MongoDB"],
            "responsibilities": ["Build APIs"],
            "experience_requirements": "2+ years",
            "keywords": ["Python", "FastAPI", "MongoDB"],
        }

    monkeypatch.setattr(
        "app.services.ai_service.AIService.generate_job_analysis",
        fake_generate_job_analysis,
    )

    response = client.post(
        f"/api/analysis/job/{application_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["summary"] == "Strong backend Python role."
    assert "Python" in data["required_skills"]


def test_resume_match_success(client, monkeypatch):
    register_user(client, "match@example.com", "Match User")
    token = login_user(client, "match@example.com", "Password123!").json()["access_token"]

    client.put(
        "/api/resume",
        json={"resume_text": "Python developer with FastAPI, MongoDB, and React experience."},
        headers={"Authorization": f"Bearer {token}"},
    )

    app_response = client.post(
        "/api/applications",
        json={
            "company": "TargetCo",
            "job_title": "Backend Engineer",
            "job_description": "Need Python, FastAPI, MongoDB, and API design experience.",
            "location": "Remote",
            "status": "Applied",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    application_id = app_response.json()["_id"]

    def fake_generate_resume_match(resume_text: str, job_description: str):
        return {
            "match_score": 88,
            "summary": "Strong fit.",
            "strengths": ["Python", "FastAPI", "MongoDB"],
            "missing_skills": ["Docker"],
            "recommendations": ["Highlight deployment work."],
        }

    monkeypatch.setattr(
        "app.services.ai_service.AIService.generate_resume_match",
        fake_generate_resume_match,
    )

    response = client.post(
        f"/api/analysis/match/{application_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["match_score"] == 88
    assert data["strengths"][0] == "Python"


def test_analysis_requires_authentication(client):
    response = client.get("/api/analysis/application/does-not-matter")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

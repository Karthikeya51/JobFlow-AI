from fastapi import status


def register_user(client, payload=None):
    data = payload or {
        "name": "Test User",
        "email": "user@example.com",
        "password": "testpassword123",
    }
    response = client.post("/api/auth/register", json=data)
    return response


def login_user(client, email, password):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return response


def make_application(overrides=None):
    data = {
        "company": "Acme Corp",
        "job_title": "Senior Python Engineer",
        "location": "Remote",
        "job_url": "https://example.com/jobs/1",
        "job_description": "Build APIs and ship features.",
        "salary": "$120k",
        "status": "Applied",
        "applied_date": "2026-01-15T00:00:00",
        "notes": "Strong match for backend role.",
    }
    if overrides:
        data.update(overrides)
    return data


def test_create_application_authenticated(client):
    register_user(client, {"name": "Alice", "email": "alice@example.com", "password": "testpassword123"})
    login_response = login_user(client, "alice@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/applications",
        json=make_application(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["company"] == "Acme Corp"
    assert payload["job_title"] == "Senior Python Engineer"
    assert payload["status"] == "Applied"
    assert payload["_id"]


def test_create_application_unauthenticated(client):
    response = client.post("/api/applications", json=make_application())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user_applications(client):
    register_user(client, {"name": "Bob", "email": "bob@example.com", "password": "testpassword123"})
    login_response = login_user(client, "bob@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    client.post(
        "/api/applications",
        json=make_application({"company": "Company A"}),
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/applications",
        json=make_application({"company": "Company B", "job_title": "Frontend Engineer"}),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/api/applications", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["total"] == 2
    assert len(payload["items"]) == 2


def test_get_single_application(client):
    register_user(client, {"name": "Charlie", "email": "charlie@example.com", "password": "testpassword123"})
    login_response = login_user(client, "charlie@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/applications",
        json=make_application({"company": "Zeta"}),
        headers={"Authorization": f"Bearer {token}"},
    )
    application_id = create_response.json()["_id"]

    response = client.get(
        f"/api/applications/{application_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["company"] == "Zeta"


def test_update_application(client):
    register_user(client, {"name": "Dana", "email": "dana@example.com", "password": "testpassword123"})
    login_response = login_user(client, "dana@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/applications",
        json=make_application({"status": "Saved"}),
        headers={"Authorization": f"Bearer {token}"},
    )
    application_id = create_response.json()["_id"]

    response = client.put(
        f"/api/applications/{application_id}",
        json={"status": "Interview", "notes": "Moved to final round."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Interview"
    assert response.json()["notes"] == "Moved to final round."


def test_delete_application(client):
    register_user(client, {"name": "Evan", "email": "evan@example.com", "password": "testpassword123"})
    login_response = login_user(client, "evan@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/applications",
        json=make_application({"company": "Delete Me"}),
        headers={"Authorization": f"Bearer {token}"},
    )
    application_id = create_response.json()["_id"]

    response = client.delete(
        f"/api/applications/{application_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_search_applications(client):
    register_user(client, {"name": "Frank", "email": "frank@example.com", "password": "testpassword123"})
    login_response = login_user(client, "frank@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    client.post(
        "/api/applications",
        json=make_application({"company": "OpenAI", "job_title": "Platform Engineer"}),
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/applications",
        json=make_application({"company": "Stripe", "job_title": "Product Manager"}),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/api/applications?search=OpenAI",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["company"] == "OpenAI"


def test_filter_applications_by_status(client):
    register_user(client, {"name": "Grace", "email": "grace@example.com", "password": "testpassword123"})
    login_response = login_user(client, "grace@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    client.post(
        "/api/applications",
        json=make_application({"company": "First", "status": "Saved"}),
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/applications",
        json=make_application({"company": "Second", "status": "Interview"}),
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/api/applications?status=Saved",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["status"] == "Saved"


def test_invalid_status_rejected(client):
    register_user(client, {"name": "Heidi", "email": "heidi@example.com", "password": "testpassword123"})
    login_response = login_user(client, "heidi@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/applications",
        json=make_application({"status": "Ghost"}),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_missing_required_fields_rejected(client):
    register_user(client, {"name": "Ivan", "email": "ivan@example.com", "password": "testpassword123"})
    login_response = login_user(client, "ivan@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/applications",
        json={"company": "Acme"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_job_url_rejected(client):
    register_user(client, {"name": "Judy", "email": "judy@example.com", "password": "testpassword123"})
    login_response = login_user(client, "judy@example.com", "testpassword123")
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/applications",
        json=make_application({"job_url": "not-a-url"}),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_access_another_users_application_forbidden(client):
    register_user(client, {"name": "Karen", "email": "karen@example.com", "password": "testpassword123"})
    register_user(client, {"name": "Leo", "email": "leo@example.com", "password": "testpassword123"})

    login_response_karen = login_user(client, "karen@example.com", "testpassword123")
    login_response_leo = login_user(client, "leo@example.com", "testpassword123")
    karen_token = login_response_karen.json()["access_token"]
    leo_token = login_response_leo.json()["access_token"]

    app_response = client.post(
        "/api/applications",
        json=make_application({"company": "Private Company"}),
        headers={"Authorization": f"Bearer {karen_token}"},
    )
    app_id = app_response.json()["_id"]

    response = client.get(
        f"/api/applications/{app_id}",
        headers={"Authorization": f"Bearer {leo_token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

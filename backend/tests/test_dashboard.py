from fastapi import status


def register_and_login(client, name, email, password="testpassword123"):
    client.post(
        "/api/auth/register",
        json={"name": name, "email": email, "password": password},
    )
    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return login_response.json()["access_token"]


def create_application(client, token, payload):
    return client.post(
        "/api/applications",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )


def test_dashboard_requires_authentication(client):
    response = client.get("/api/dashboard/stats")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_dashboard_empty_user_receives_zero_stats(client):
    token = register_and_login(client, "Zero User", "zero@example.com")
    response = client.get("/api/dashboard/stats", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["summary"]["total"] == 0
    assert data["summary"]["saved"] == 0
    assert data["summary"]["applied"] == 0
    assert data["summary"]["interview"] == 0
    assert data["summary"]["offer"] == 0
    assert data["summary"]["rejected"] == 0
    assert data["conversion"]["interview_rate"] == 0.0
    assert data["conversion"]["offer_rate"] == 0.0


def test_dashboard_status_counts_and_recent_applications(client):
    token = register_and_login(client, "Alpha", "alpha@example.com")
    create_application(
        client,
        token,
        {
            "company": "Acme",
            "job_title": "Engineer",
            "location": "Remote",
            "job_url": "https://example.com/job/1",
            "job_description": "Do work.",
            "status": "Applied",
            "applied_date": "2026-07-01T00:00:00",
            "notes": "Sample",
        },
    )
    create_application(
        client,
        token,
        {
            "company": "Beta",
            "job_title": "Manager",
            "location": "NYC",
            "job_url": "https://example.com/job/2",
            "job_description": "Lead people.",
            "status": "Interview",
            "applied_date": "2026-07-05T00:00:00",
            "notes": "Sample",
        },
    )
    create_application(
        client,
        token,
        {
            "company": "Gamma",
            "job_title": "Analyst",
            "location": "SF",
            "job_url": "https://example.com/job/3",
            "job_description": "Analyze data.",
            "status": "Offer",
            "applied_date": "2026-07-10T00:00:00",
            "notes": "Sample",
        },
    )

    response = client.get("/api/dashboard/stats", headers={"Authorization": f"Bearer {token}"})
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["summary"]["total"] == 3
    assert data["summary"]["applied"] == 1
    assert data["summary"]["interview"] == 1
    assert data["summary"]["offer"] == 1
    assert data["summary"]["rejected"] == 0
    assert len(data["recent_applications"]) == 3
    assert data["status_distribution"][1]["status"] == "Applied"
    assert data["status_distribution"][1]["count"] == 1


def test_dashboard_trend_and_conversion(client):
    token = register_and_login(client, "Trend User", "trend@example.com")
    create_application(
        client,
        token,
        {
            "company": "X1",
            "job_title": "Dev",
            "job_description": "Work.",
            "status": "Applied",
            "applied_date": "2026-05-05T00:00:00",
        },
    )
    create_application(
        client,
        token,
        {
            "company": "X2",
            "job_title": "Dev2",
            "job_description": "Work more.",
            "status": "Interview",
            "applied_date": "2026-06-05T00:00:00",
        },
    )
    create_application(
        client,
        token,
        {
            "company": "X3",
            "job_title": "Dev3",
            "job_description": "Work more.",
            "status": "Offer",
            "applied_date": "2026-07-05T00:00:00",
        },
    )

    response = client.get("/api/dashboard/stats", headers={"Authorization": f"Bearer {token}"})
    data = response.json()

    assert data["conversion"]["interview_rate"] == 66.67
    assert data["conversion"]["offer_rate"] == 33.33
    assert len(data["monthly_trend"]) == 6
    assert sum(item["count"] for item in data["monthly_trend"]) == 3


def test_dashboard_user_isolation(client):
    user_a_token = register_and_login(client, "User A", "usera@example.com")
    user_b_token = register_and_login(client, "User B", "userb@example.com")

    create_application(
        client,
        user_a_token,
        {
            "company": "A Company",
            "job_title": "A Job",
            "job_description": "A role.",
            "status": "Applied",
            "applied_date": "2026-07-01T00:00:00",
        },
    )
    create_application(
        client,
        user_a_token,
        {
            "company": "A Company 2",
            "job_title": "A Job 2",
            "job_description": "Another role.",
            "status": "Offer",
            "applied_date": "2026-07-02T00:00:00",
        },
    )
    create_application(
        client,
        user_b_token,
        {
            "company": "B Company",
            "job_title": "B Job",
            "job_description": "B role.",
            "status": "Rejected",
            "applied_date": "2026-07-03T00:00:00",
        },
    )

    a_response = client.get("/api/dashboard/stats", headers={"Authorization": f"Bearer {user_a_token}"})
    b_response = client.get("/api/dashboard/stats", headers={"Authorization": f"Bearer {user_b_token}"})

    assert a_response.status_code == status.HTTP_200_OK
    assert b_response.status_code == status.HTTP_200_OK
    assert a_response.json()["summary"]["total"] == 2
    assert b_response.json()["summary"]["total"] == 1
    assert a_response.json()["summary"]["offer"] == 1
    assert b_response.json()["summary"]["rejected"] == 1

import pytest
from fastapi import status


def test_health_check(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"


def test_register_success(client, test_user_data):
    """Test successful user registration"""
    response = client.post("/api/auth/register", json=test_user_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == test_user_data["name"]
    assert data["email"] == test_user_data["email"]
    assert "_id" in data
    assert "created_at" in data


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email"""
    # Register first user
    client.post("/api/auth/register", json=test_user_data)
    
    # Try to register with same email
    response = client.post("/api/auth/register", json=test_user_data)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Email already registered" in response.json()["detail"]


def test_register_invalid_email(client):
    """Test registration with invalid email"""
    invalid_data = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "testpassword123",
    }
    response = client.post("/api/auth/register", json=invalid_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_short_password(client):
    """Test registration with password too short"""
    invalid_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "short",
    }
    response = client.post("/api/auth/register", json=invalid_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_success(client, test_user_data):
    """Test successful login"""
    # Register first
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"],
    }
    response = client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == test_user_data["email"]


def test_login_invalid_email(client, test_user_data):
    """Test login with non-existent email"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password123",
    }
    response = client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid email or password" in response.json()["detail"]


def test_login_wrong_password(client, test_user_data):
    """Test login with wrong password"""
    # Register first
    client.post("/api/auth/register", json=test_user_data)
    
    # Try login with wrong password
    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword123",
    }
    response = client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid email or password" in response.json()["detail"]


def test_get_current_user_success(client, test_user_data):
    """Test getting current user with valid token"""
    # Register and login
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"],
        },
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]


def test_get_current_user_no_token(client):
    """Test getting current user without token"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing or invalid authorization header" in response.json()["detail"]


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token_12345"},
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid or expired token" in response.json()["detail"]


def test_get_current_user_malformed_header(client, test_user_data):
    """Test getting current user with malformed auth header"""
    # Register and login
    client.post("/api/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"],
        },
    )
    token = login_response.json()["access_token"]
    
    # Send malformed header
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"InvalidPrefix {token}"},
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

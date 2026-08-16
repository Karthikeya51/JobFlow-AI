import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_database


@pytest.fixture
def test_db():
    """Get test database"""
    db = get_database()
    db["users"].delete_many({})
    db["applications"].delete_many({})
    db["resume_profiles"].delete_many({})
    db["ai_analyses"].delete_many({})
    yield db
    db["users"].delete_many({})
    db["applications"].delete_many({})
    db["resume_profiles"].delete_many({})
    db["ai_analyses"].delete_many({})


@pytest.fixture
def client():
    """Test client for API"""
    db = get_database()
    db["users"].delete_many({})
    db["applications"].delete_many({})
    db["resume_profiles"].delete_many({})
    db["ai_analyses"].delete_many({})
    with TestClient(app) as test_client:
        yield test_client
    db["users"].delete_many({})
    db["applications"].delete_many({})
    db["resume_profiles"].delete_many({})
    db["ai_analyses"].delete_many({})


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123",
    }

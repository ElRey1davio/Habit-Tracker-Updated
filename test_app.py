import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
def test_index_requires_login(client):
    response = client.get("/")
    assert response.status_code == 401
    
def test_login_with_wrong_password_fails(client):
    response = client.post("/login", json={"username": "papi", "password": "1234567"})
    assert response.status_code == 401
    
import random

def test_register_and_login_succeeds(client):
    username = f"testuser{random.randint(1, 999999)}"
    password = "testpassword123"

    register_response = client.post("/register", json={"username": username, "password": password})
    assert register_response.status_code == 200

    login_response = client.post("/login", json={"username": username, "password": password})
    assert login_response.status_code == 200
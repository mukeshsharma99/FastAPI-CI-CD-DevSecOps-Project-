from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "FastAPI + PostgreSQL is working"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "pytest_create_101@example.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "pytest_create_101@example.com"
    assert "id" in data


def test_get_user_by_id():
    response = client.post(
        "/users",
        json={
            "name": "Get Test User",
            "email": "pytest_get_102@example.com"
        }
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["name"] == "Get Test User"
    assert response.json()["email"] == "pytest_get_102@example.com"


def test_get_user_not_found():
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user():
    response = client.post(
        "/users",
        json={
            "name": "Before Update",
            "email": "pytest_update_103@example.com"
        }
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "name": "After Update",
            "email": "pytest_updated_104@example.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "After Update"
    assert data["email"] == "pytest_updated_104@example.com"


def test_delete_user():
    response = client.post(
        "/users",
        json={
            "name": "Delete Test User",
            "email": "pytest_delete_105@example.com"
        }
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404


def test_duplicate_email():
    email = "pytest_duplicate_106@example.com"

    response = client.post(
        "/users",
        json={
            "name": "First User",
            "email": email
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/users",
        json={
            "name": "Second User",
            "email": email
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
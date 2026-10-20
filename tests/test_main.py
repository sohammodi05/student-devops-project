
from fastapi.testclient import TestClient
from main import app, students

client = TestClient(app)


def setup_function():
    students.clear()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_student():
    response = client.post(
        "/students",
        json={
            "id": 1,
            "name": "Rahul Patel",
            "email": "rahul@example.com",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_duplicate_student():
    student = {
        "id": 1,
        "name": "Rahul Patel",
        "email": "rahul@example.com",
    }

    client.post("/students", json=student)
    response = client.post("/students", json=student)

    assert response.status_code == 409


def test_student_not_found():
    response = client.get("/students/999")
    assert response.status_code == 404


def test_delete_student():
    student = {
        "id": 1,
        "name": "Rahul Patel",
        "email": "rahul@example.com",
    }

    client.post("/students", json=student)
    response = client.delete("/students/1")

    assert response.status_code == 200
    assert client.get("/students/1").status_code == 404

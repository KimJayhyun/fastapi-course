from test.utils import TestingSessionLocal, client

from fastapi import status
from models import Todos


def test_read_all_authenticated(test_todo: Todos):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "Test todo",
            "description": "Test description",
            "priority": 1,
            "completed": False,
            "owner_id": 1,
        }
    ]


def test_read_one_authenticated(test_todo: Todos):
    response = client.get("/todo/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Test todo",
        "description": "Test description",
        "priority": 1,
        "completed": False,
        "owner_id": 1,
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "New Test todo",
        "description": "New Test description",
        "priority": 5,
        "completed": False,
    }

    response = client.post("/todos", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.completed == request_data["completed"]


def test_update_todo(test_todo):
    request_data = {
        "title": "Updated Test todo",
        "description": "Updated Test description",
        "priority": 5,
        "completed": False,
    }

    response = client.put("/todo/1", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.completed == request_data["completed"]


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Updated Test todo",
        "description": "Updated Test description",
        "priority": 5,
        "completed": False,
    }

    response = client.put("/todo/999", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


def test_delete_todo(test_todo):
    response = client.delete("/todo/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    assert response.json() == {"detail": "Todo not found"}
    assert response.json() == {"detail": "Todo not found"}

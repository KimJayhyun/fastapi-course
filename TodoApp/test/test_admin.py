from test.utils import TestingSessionLocal, client

from fastapi import status
from models import Todos


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")

    print(response.json())

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


def test_admin_test_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


def test_admin_test_delete_todo(test_todo):
    response = client.delete("/admin/todo/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}

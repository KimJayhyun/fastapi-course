from test.utils import client

from fastapi import status


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

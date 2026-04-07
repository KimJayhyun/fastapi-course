from test.utils import client

from fastapi import status


def test_return_user(test_user):
    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "Test user"
    assert response.json().get("email") == "a@b.com"
    assert response.json().get("first_name") == "Test"
    assert response.json().get("last_name") == "User"
    assert response.json().get("role") == "admin"
    assert response.json().get("phone_number") == "123-456-7890"


def test_change_password_success(test_user):
    response = client.put(
        "/user/password", json={"password": "test", "new_password": "new_password"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/password", json={"password": "wrong", "new_password": "new_password"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Error on password change"


def test_change_phone_number_success(test_user):
    response = client.put(
        "/user/phone_number",
        json={"password": "test", "new_phone_number": "123-456-7891"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "Test user"
    assert response.json().get("email") == "a@b.com"
    assert response.json().get("first_name") == "Test"
    assert response.json().get("last_name") == "User"
    assert response.json().get("role") == "admin"
    assert response.json().get("phone_number") == "123-456-7891"

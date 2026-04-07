from datetime import timedelta
from test.utils import TestingSessionLocal, client

import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt
from routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
)


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "test", db)
    assert authenticated_user is not None
    assert authenticated_user.id == test_user.id

    non_existent_user = authenticate_user("Non-existent user", "test", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrong", db)
    assert wrong_password_user is False


def test_create_access_token(test_user):
    expires_delta = timedelta(days=1)

    token = create_access_token(
        test_user.username, test_user.id, test_user.role, expires_delta
    )
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_token.get("sub") == test_user.username
    assert decoded_token.get("id") == test_user.id
    assert decoded_token.get("role") == test_user.role


@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_user):
    encode = {
        "sub": test_user.username,
        "id": test_user.id,
        "role": test_user.role,
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)

    assert user.get("username") == test_user.username
    assert user.get("id") == test_user.id
    assert user.get("role") == test_user.role


@pytest.mark.asyncio
async def test_get_current_user_missing_payload(test_user):
    encode = {
        "sub": test_user.username,
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate user."

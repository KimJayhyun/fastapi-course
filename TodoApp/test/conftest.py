from test.utils import TestingSessionLocal, engine

import pytest
from models import Todos, Users
from routers.user import bcrypt_context


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test todo",
        description="Test description",
        priority=1,
        completed=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo

    with engine.connect() as connection:
        connection.execute(Todos.__table__.delete())
        # connection.execute(text("DELETE FROM todos;"))

        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="Test user",
        email="a@b.com",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("test"),
        role="admin",
        phone_number="123-456-7890",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user

    with engine.connect() as connection:
        connection.execute(Users.__table__.delete())

        connection.commit()

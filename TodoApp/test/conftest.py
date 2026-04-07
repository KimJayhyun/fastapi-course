from test.utils import TestingSessionLocal, engine

import pytest
from models import Todos


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

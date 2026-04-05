"""Create phone number for user column

Revision ID: 66ce6f16ea8d
Revises:
Create Date: 2026-04-04 17:34:36.820852

"""

from typing import Sequence, Union

import models
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "66ce6f16ea8d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone_number")

"""add unique interview booking constraint

Revision ID: 68af79c45fd5
Revises: 56a4b3c8702e
Create Date: 2026-11-18 13:48:37.813283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68af79c45fd5'
down_revision: Union[str, Sequence[str], None] = '56a4b3c8702e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_unique_constraint(
        "uq_interview_booking_email_date_time",
        "interview_bookings",
        ["email", "interview_date", "interview_time"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_interview_booking_email_date_time",
        "interview_bookings",
        type_="unique",
    )
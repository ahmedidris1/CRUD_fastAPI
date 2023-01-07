"""add content column to posts table

Revision ID: e4eea368f7fe
Revises: 4897a0bee466
Create Date: 2023-01-06 15:22:56.072834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4eea368f7fe'
down_revision = '4897a0bee466'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")

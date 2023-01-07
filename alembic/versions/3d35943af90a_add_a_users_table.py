"""add a users table

Revision ID: 3d35943af90a
Revises: e4eea368f7fe
Create Date: 2023-01-06 16:24:23.632322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d35943af90a'
down_revision = 'e4eea368f7fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.sql.sqltypes.TIMESTAMP(timezone=True),
                              server_default=sa.sql.text("NOW()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )


def downgrade() -> None:
    op.drop_table("users")

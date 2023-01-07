"""add few columns to posts table

Revision ID: 65de2cd03b6e
Revises: 6c46c4f06554
Create Date: 2023-01-06 17:31:16.728699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65de2cd03b6e'
down_revision = '6c46c4f06554'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column( "posts", 
                  sa.Column("published", sa.Boolean(), server_default="True", nullable=False)
                  )
    op.add_column( "posts", 
                  sa.Column("created_at", sa.sql.sqltypes.TIMESTAMP(timezone=True), 
                            server_default=sa.sql.text("NOW()"), nullable=False)
                  )


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="published")
    op.drop_column(table_name="posts", column_name="created_at")

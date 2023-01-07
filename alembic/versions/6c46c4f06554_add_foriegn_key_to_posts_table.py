"""add foriegn-key to posts table

Revision ID: 6c46c4f06554
Revises: 3d35943af90a
Create Date: 2023-01-06 17:06:10.297202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c46c4f06554'
down_revision = '3d35943af90a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column( "posts", sa.Column("author_id", sa.Integer, nullable=False) )
    op.create_foreign_key(constraint_name="posts_users_fk", 
                          source_table="posts", referent_table="users",
                          local_cols=["author_id"], remote_cols=["id"],
                          ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column(table_name="posts", column_name="author_id")

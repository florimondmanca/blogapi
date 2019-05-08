"""add index on created and modified

Revision ID: 841a5eee0b81
Revises: e1f6c3d09f44
Create Date: 2019-05-08 20:33:48.709376

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "841a5eee0b81"
down_revision = "e1f6c3d09f44"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        op.f("ix_posts_created"), "posts", ["created"], unique=False
    )
    op.create_index(
        op.f("ix_posts_modified"), "posts", ["modified"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_posts_modified"), table_name="posts")
    op.drop_index(op.f("ix_posts_created"), table_name="posts")

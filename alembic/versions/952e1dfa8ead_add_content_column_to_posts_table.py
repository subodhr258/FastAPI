"""add content column to posts table

Revision ID: 952e1dfa8ead
Revises: c8b37c293de6
Create Date: 2023-01-16 14:44:49.438580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '952e1dfa8ead'
down_revision = 'c8b37c293de6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')

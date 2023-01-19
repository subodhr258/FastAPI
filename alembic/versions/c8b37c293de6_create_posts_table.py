"""create posts table

Revision ID: c8b37c293de6
Revises: 
Create Date: 2023-01-16 00:56:56.370542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8b37c293de6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')

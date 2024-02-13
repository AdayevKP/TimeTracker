"""init

Revision ID: dd199aaef2dd
Revises: 
Create Date: 2024-02-13 11:16:09.951557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd199aaef2dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'time_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
        sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('time_entries')
    op.drop_table('projects')

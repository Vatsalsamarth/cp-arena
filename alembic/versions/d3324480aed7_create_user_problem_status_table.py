"""create user_problem_status table

Revision ID: d3324480aed7
Revises: bf1e25c3ce40
Create Date: 2026-07-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3324480aed7'
down_revision: Union[str, Sequence[str], None] = 'bf1e25c3ce40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user_problem_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('problem_id', sa.Integer(), nullable=False),
        sa.Column('first_solved_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'problem_id', name='uq_user_problem_status_user_problem'),
    )
    op.create_index(op.f('ix_user_problem_status_id'), 'user_problem_status', ['id'], unique=False)
    op.create_index(op.f('ix_user_problem_status_user_id'), 'user_problem_status', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_problem_status_problem_id'), 'user_problem_status', ['problem_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_problem_status_problem_id'), table_name='user_problem_status')
    op.drop_index(op.f('ix_user_problem_status_user_id'), table_name='user_problem_status')
    op.drop_index(op.f('ix_user_problem_status_id'), table_name='user_problem_status')
    op.drop_table('user_problem_status')

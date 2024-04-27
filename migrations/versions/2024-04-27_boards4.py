"""boards4

Revision ID: 0f2b0a32550a
Revises: 17dcc7874a0b
Create Date: 2024-04-27 17:50:38.888740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f2b0a32550a'
down_revision: Union[str, None] = '17dcc7874a0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('winner', sa.String(), nullable=True))
    op.add_column('move', sa.Column('board_prev_state', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('move', 'board_prev_state')
    op.drop_column('board', 'winner')
    # ### end Alembic commands ###

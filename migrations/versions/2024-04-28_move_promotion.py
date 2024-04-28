"""move_promotion

Revision ID: ffa0386ba730
Revises: 0f2b0a32550a
Create Date: 2024-04-28 22:20:25.381953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffa0386ba730'
down_revision: Union[str, None] = '0f2b0a32550a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('move', sa.Column('promotion', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('move', 'promotion')
    # ### end Alembic commands ###
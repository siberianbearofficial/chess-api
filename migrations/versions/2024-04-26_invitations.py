"""invitations

Revision ID: 73f57873c018
Revises: 445073be0047
Create Date: 2024-04-26 17:25:34.245336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73f57873c018'
down_revision: Union[str, None] = '445073be0047'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invitation',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('board', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['board'], ['board.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invitation')
    # ### end Alembic commands ###
from uuid import uuid4

from sqlalchemy import Column, String, Uuid, DateTime, ForeignKey

from utils.database import Base

from moves.schemas import MoveRead

from boards.models import Board


class Move(Base):
    __tablename__ = 'move'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    board = Column(Uuid, ForeignKey(Board.uuid), nullable=False)
    actor = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    src = Column(String, nullable=False)
    dst = Column(String, nullable=False)
    figure = Column(String, nullable=False)
    board_prev_state = Column(String, nullable=False)

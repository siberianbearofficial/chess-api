from uuid import uuid4

from sqlalchemy import Column, String, Uuid, DateTime, ForeignKey

from boards.models import Board

from utils.models import IModel


class Move(IModel):
    __tablename__ = 'move'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    board = Column(Uuid, ForeignKey(Board.uuid), nullable=False)
    actor = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    src = Column(String, nullable=False)
    dst = Column(String, nullable=False)
    figure = Column(String, nullable=False)
    board_prev_state = Column(String, nullable=False)

    def dict(self):
        return {
            'uuid': self.uuid,
            'board': self.board,
            'actor': self.actor,
            'created_at': self.created_at,
            'src': self.src,
            'dst': self.dst,
            'figure': self.figure,
            'board_prev_state': self.board_prev_state
        }

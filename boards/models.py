from uuid import uuid4, UUID
from json import loads
import chess

from sqlalchemy import Column, String, Uuid, DateTime

from utils.database import Base

from boards.schemas import BoardRead


class Board(Base):
    __tablename__ = 'board'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    owner = Column(Uuid, nullable=False)
    mode = Column(String, nullable=False)
    privacy = Column(String, nullable=False)
    invited = Column(String, nullable=False)
    white = Column(Uuid, nullable=True)
    black = Column(Uuid, nullable=True)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    state = Column(String, nullable=False)

    def to_read_model(self):
        return BoardRead(
            uuid=self.uuid,
            owner=self.owner,
            mode=self.mode,
            privacy=self.privacy,
            invited=[UUID(s) for s in loads(self.invited)],
            white=self.white,
            black=self.black,
            created_at=self.created_at,
            state=board_state_from_str(self.state)
        )


def board_state_from_str(state):
    board = chess.Board(state)
    print(board)
    return {
        'a1': {
            'figure': 'queen',
            'actor': 'white'
        }
    }

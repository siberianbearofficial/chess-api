from sqlalchemy import Column, String, Uuid, DateTime

from utils.models import IModel


class Board(IModel):
    __tablename__ = 'board'

    uuid = Column(Uuid, primary_key=True, nullable=False)
    owner = Column(Uuid, nullable=False)
    mode = Column(String, nullable=False)
    privacy = Column(String, nullable=False)
    invited = Column(String, nullable=False)
    white = Column(Uuid, nullable=True)
    black = Column(Uuid, nullable=True)
    winner = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    state = Column(String, nullable=False)

    def dict(self):
        return {
            'uuid': self.uuid,
            'owner': self.owner,
            'mode': self.mode,
            'privacy': self.privacy,
            'invited': self.invited,
            'white': self.white,
            'black': self.black,
            'winner': self.winner,
            'created_at': self.created_at,
            'status': self.status,
            'state': self.state
        }

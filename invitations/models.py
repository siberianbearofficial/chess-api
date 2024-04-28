from sqlalchemy import Column, String, Uuid, DateTime, ForeignKey

from boards.models import Board

from utils.models import IModel


class Invitation(IModel):
    __tablename__ = 'invitation'

    code = Column(String, primary_key=True)
    board = Column(Uuid, ForeignKey(Board.uuid), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def dict(self):
        return {
            'code': self.code,
            'board': self.board,
            'created_at': self.created_at
        }

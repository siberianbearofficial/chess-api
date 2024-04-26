from sqlalchemy import Column, String, Uuid, DateTime, ForeignKey

from utils.database import Base

from invitations.schemas import InvitationRead

from boards.models import Board


class Invitation(Base):
    __tablename__ = 'invitation'

    code = Column(String, primary_key=True)
    board = Column(Uuid, ForeignKey(Board.uuid), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def to_read_model(self):
        return InvitationRead(
            code=self.code,
            board=self.board,
            created_at=self.created_at
        )

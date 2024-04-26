from uuid import uuid4

from sqlalchemy import Column, String, Uuid, DateTime, ForeignKey

from utils.database import Base

from invitations.schemas import InvitationRead

from boards.models import Board


class Invitation(Base):
    __tablename__ = 'invitation'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    board = Column(Uuid, ForeignKey(Board.uuid), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def to_read_model(self):
        return InvitationRead(
            uuid=self.uuid,
            code=self.code,
            board=self.board,
            created_at=self.created_at
        )

from sqlalchemy import Column, String, Uuid, DateTime

from utils.database import Base


class Board(Base):
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

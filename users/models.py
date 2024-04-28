import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, String, Uuid

from utils.models import IModel


class User(IModel):
    __tablename__ = 'user'

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(tz=None))
    roles = Column(String)
    hashed_password: str = Column(String(length=1024), nullable=False)

    def dict(self):
        return {
            'uuid': self.uuid,
            'username': self.username,
            'hashed_password': self.hashed_password,
            'created_at': self.created_at,
            'roles': self.roles
        }

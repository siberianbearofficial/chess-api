import uuid

from sqlalchemy import Column, String, Uuid

from utils.models import IModel


class Role(IModel):
    __tablename__ = 'role'

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    permissions = Column(String)

    def dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'permissions': self.permissions
        }

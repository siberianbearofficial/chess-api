from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class InvitationRead(BaseModel):
    code: str
    board: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class InvitationCreate(BaseModel):
    board: UUID

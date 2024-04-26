from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class BoardCell(BaseModel):
    figure: str
    actor: str


class BoardRead(BaseModel):
    uuid: UUID
    owner: UUID
    mode: str
    privacy: str
    invited: list[UUID]
    white: UUID | None
    black: UUID | None
    created_at: datetime
    status: str
    state: dict[str, BoardCell]

    class Config:
        from_attributes = True


class BoardCreate(BaseModel):
    owner: UUID
    mode: str
    privacy: str


class BoardUpdate(BaseModel):
    name: str
    permissions: list[str]

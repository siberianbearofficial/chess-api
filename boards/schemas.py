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
    winner: str | None
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
    mode: str | None
    privacy: str | None
    invited: list[UUID] | None
    white: UUID | None
    black: UUID | None


class BoardInvite(BaseModel):
    invitation: str
    invited: UUID

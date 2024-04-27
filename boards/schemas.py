from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from uuid import UUID


class BoardCell(BaseModel):
    figure: Literal['queen', 'king', 'rook', 'bishop', 'knight', 'pawn']
    actor: Literal['white', 'black']


class BoardRead(BaseModel):
    uuid: UUID
    owner: UUID
    mode: Literal['online']
    privacy: Literal['private']
    invited: list[UUID]
    white: UUID | None
    black: UUID | None
    winner: Literal['white', 'black'] | None
    created_at: datetime
    status: str  # тут бы перечислить возможные статусы, но многие пока напрямую возвращаются либой
    state: dict[str, BoardCell]

    class Config:
        from_attributes = True


class BoardCreate(BaseModel):
    owner: UUID
    mode: Literal['online']
    privacy: Literal['private']


class BoardUpdate(BaseModel):
    mode: Literal['online'] | None
    privacy: Literal['private'] | None
    invited: list[UUID] | None
    white: UUID | None
    black: UUID | None


class BoardInvite(BaseModel):
    invitation: str  # 6-digit code тоже валидировать надо бы
    invited: UUID

from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from uuid import UUID


class MoveRead(BaseModel):
    uuid: UUID
    board: UUID
    actor: Literal['white', 'black']
    created_at: datetime
    src: str  # по-хорошему, тут нужно написать кастомные валидаторы, чтобы pydantic по ним отсекал все неподходящее
    dst: str
    figure: Literal['queen', 'king', 'rook', 'bishop', 'knight', 'pawn']

    class Config:
        from_attributes = True


class MoveCreate(BaseModel):
    board: UUID
    actor: Literal['white', 'black'] | None = None
    src: str
    dst: str


class LegalMove(BaseModel):
    board: UUID
    actor: Literal['white', 'black']
    src: str
    dst: str
    figure: Literal['queen', 'king', 'rook', 'bishop', 'knight', 'pawn'] | None

    class Config:
        from_attributes = True

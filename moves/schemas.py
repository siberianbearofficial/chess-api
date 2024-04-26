from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class MoveRead(BaseModel):
    uuid: UUID
    board: UUID
    actor: str  # white | black
    created_at: datetime
    src: str
    dst: str
    figure: str

    class Config:
        from_attributes = True


class MoveCreate(BaseModel):
    board: UUID
    actor: str | None = None  # white | black    и все-таки что-то тут не так...
    src: str
    dst: str


class MoveUndo(BaseModel):
    board: UUID
    actor: str  # white | black

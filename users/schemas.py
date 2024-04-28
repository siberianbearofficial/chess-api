from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserRead(BaseModel):
    uuid: UUID
    username: str
    created_at: datetime
    roles: list[UUID]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    roles: list[UUID] = []


class UserUpdate(BaseModel):
    username: str = ''
    roles: list[UUID] = []


class UserWithPassword(BaseModel):
    uuid: UUID
    username: str
    hashed_password: str
    created_at: datetime
    roles: list[UUID]

    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    current_password: str
    new_password: str

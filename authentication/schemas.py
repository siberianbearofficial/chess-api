import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AuthenticationCreate(BaseModel):
    username: str  # надо длину и прочие проверки валидности на pydantic переложить
    password: str


class AuthenticationRead(BaseModel):
    token_type: Literal['Bearer']
    access_token: str
    expires_at: datetime
    user_uuid: uuid.UUID
    roles: list[uuid.UUID]

    class Config:
        from_attributes = True

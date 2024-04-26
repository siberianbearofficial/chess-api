from datetime import datetime, timedelta
from typing import Iterable
from uuid import UUID
import jwt

from utils.config import AUTHENTICATION_SECRET


async def get_payload(uuid: UUID, roles: Iterable):
    payload = {
        'exp': (datetime.now() + timedelta(days=30)).timestamp(),
        'sub': str(uuid),
        'roles': [str(role_uuid) for role_uuid in roles]
    }
    encoded_jwt = jwt.encode(payload, AUTHENTICATION_SECRET, algorithm='HS256')
    payload.update({'access_token': encoded_jwt, 'token_type': 'Bearer'})
    return payload

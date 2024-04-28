from datetime import datetime, timedelta
import jwt
import json
import uuid

from authentication.exceptions import IncorrectCredentialsError, NotAuthenticatedError
from authentication.schemas import AuthenticationCreate, AuthenticationRead

from users.repository import UsersRepository
from users.service import UsersService
from utils.logic import check_password

from utils.unitofwork import IUnitOfWork
from utils.config import AUTHENTICATION_SECRET


class AuthenticationService:
    expiration_timedelta = timedelta(days=30)

    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def authenticated_user(self, uow: IUnitOfWork, authorization: str | None):
        async with uow:
            if not authorization:
                return None

            token = authorization.strip().split()
            if len(token) <= 1:
                return None

            token_type, access_token = token
            if token_type.strip().lower() != 'bearer':
                return None

            try:
                payload = jwt.decode(access_token.strip(), AUTHENTICATION_SECRET, algorithms=['HS256'])
            except Exception as e:
                print(e)
                return None

            if not payload['sub']:
                return None

            user_dict = await self.users_repository.get(uow.session, uuid=uuid.UUID(payload['sub']))
            if not user_dict:
                return None
            return UsersService.users_dict_to_read_model(user_dict)

    async def authenticate(self, uow: IUnitOfWork, authentication: AuthenticationCreate):
        async with uow:
            users_dict = await self.users_repository.get_all(uow.session, username=authentication.username)
            if not users_dict:
                raise NotAuthenticatedError

            if not check_password(authentication.password, users_dict[0]['hashed_password']):
                raise IncorrectCredentialsError

            expires_at = datetime.now(tz=None) + self.expiration_timedelta
            authentication_dict = {
                'expires_at': expires_at,
                'user_uuid': users_dict[0]['uuid'],
                'roles': users_dict[0]['roles'],
                'access_token': jwt.encode({
                    'exp': expires_at.timestamp(),
                    'sub': str(users_dict[0]['uuid'])
                }, AUTHENTICATION_SECRET, algorithm='HS256')
            }
            return self.authentication_dict_to_read_model(authentication_dict)

    @staticmethod
    def authentication_dict_to_read_model(authentication_dict: dict) -> AuthenticationRead:
        return AuthenticationRead(
            expires_at=authentication_dict['expires_at'],
            user_uuid=authentication_dict['user_uuid'],
            roles=json.loads(authentication_dict['roles']),
            access_token=authentication_dict['access_token'],
            token_type='Bearer'
        )

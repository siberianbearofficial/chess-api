from datetime import datetime
import json
import uuid

from users.logic import validate_username
from utils.unitofwork import IUnitOfWork
from utils.logic import hash_password

from users.repository import UsersRepository
from users.schemas import UserCreate, UserUpdate, ChangePassword, UserRead, UserWithPassword


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def get_users(self, uow: IUnitOfWork,
                        username: str | None = None,
                        with_password: bool = False) -> list[UserRead] | list[UserWithPassword]:
        async with uow:
            filter_by_dict = {'username': username} if username else {}
            users_dict = await self.users_repository.get_all(uow.session, **filter_by_dict)
            if with_password:
                return [self.users_dict_to_with_password_model(user_dict) for user_dict in users_dict]
            return [self.users_dict_to_read_model(user_dict) for user_dict in users_dict]

    async def get_user(self, uow: IUnitOfWork, user_uuid: uuid.UUID, with_password: bool = False) -> UserRead | UserWithPassword | None:
        async with uow:
            user_dict = await self.users_repository.get(uow.session, uuid=user_uuid)
            if not user_uuid:
                return None
            if with_password:
                return self.users_dict_to_with_password_model(user_dict)
            return self.users_dict_to_read_model(user_dict)

    @staticmethod
    def users_dict_to_read_model(users_dict: dict) -> UserRead:
        return UserRead(
            uuid=users_dict['uuid'],
            username=users_dict['username'],
            created_at=users_dict['created_at'],
            roles=json.loads(users_dict['roles'])
        )

    @staticmethod
    def users_dict_to_with_password_model(users_dict: dict) -> UserWithPassword:
        return UserWithPassword(
            uuid=users_dict['uuid'],
            username=users_dict['username'],
            created_at=users_dict['created_at'],
            roles=json.loads(users_dict['roles']),
            hashed_password=users_dict['hashed_password']
        )

    @staticmethod
    def users_create_model_to_dict(user: UserCreate) -> dict:
        return {
            'uuid': uuid.uuid4(),
            'username': user.username,
            'created_at': datetime.now(tz=None),
            'roles': json.dumps([str(role_uuid) for role_uuid in user.roles])
        }

    @staticmethod
    def users_update_model_to_dict(user: UserUpdate, full: bool = False) -> dict:
        user_dict = dict()
        if user.username:
            validate_username(user.username)
            user_dict['username'] = user.username
        if full:
            user_dict['roles'] = json.dumps([str(role_uuid) for role_uuid in user.roles])
        return user_dict

    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        async with uow:
            user_dict = self.users_create_model_to_dict(user)
            user_dict['hashed_password'] = hash_password(user.password)
            await self.users_repository.add(uow.session, user_dict)
            await uow.commit()
            return user_dict['uuid']

    async def update_user(self, uow: IUnitOfWork, user_uuid: uuid.UUID, user: UserUpdate, full_update: bool = False):
        async with uow:
            user_dict = self.users_update_model_to_dict(user, full_update)
            await self.users_repository.edit(uow.session, user_uuid, user_dict)
            await uow.commit()
            return user_uuid

    async def change_password(self, uow: IUnitOfWork, user_uuid: uuid.UUID, change_password: ChangePassword):
        async with uow:
            await self.users_repository.edit(uow.session, user_uuid, {
                'hashed_password': hash_password(change_password.new_password)
            })
            await uow.commit()
            return user_uuid

    async def delete_user(self, uow: IUnitOfWork, user_uuid: uuid.UUID):
        async with uow:
            await self.users_repository.delete(uow.session, user_uuid)
            await uow.commit()
            return user_uuid

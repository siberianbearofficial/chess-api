import uuid
import json
from typing import Iterable

from utils.unitofwork import IUnitOfWork

from users.schemas import UserRead, UserCreate, UserUpdate

from roles.repository import RolesRepository
from roles.schemas import RoleCreate, RoleUpdate, RoleRead


class RolesService:
    def __init__(self, roles_repository: RolesRepository):
        self.roles_repository = roles_repository

    async def get_roles(self, uow: IUnitOfWork,
                        name: str | None = None,
                        as_dict: bool = False) -> list[RoleRead] | list[dict]:
        filter_by = {'name': name} if name else {}
        async with uow:
            roles_dict = await self.roles_repository.get_all(uow.session, **filter_by)
            if as_dict:
                return roles_dict
            return [self.roles_dict_to_read_model(role_dict) for role_dict in roles_dict]

    async def get_role(self, uow: IUnitOfWork, role_uuid: uuid.UUID, as_dict: bool = False) -> RoleRead | dict | None:
        async with uow:
            role_dict = await self.roles_repository.get(uow.session, uuid=role_uuid)
            if not role_dict:
                return None
            if as_dict:
                return role_dict
            return self.roles_dict_to_read_model(role_dict)

    @staticmethod
    def roles_dict_to_read_model(role_dict: dict) -> RoleRead:
        return RoleRead(
            uuid=role_dict['uuid'],
            name=role_dict['name'],
            permissions=json.loads(role_dict['permissions'])
        )

    @staticmethod
    def roles_create_model_to_dict(role: RoleCreate) -> dict:
        return {
            'uuid': uuid.uuid4(),
            'name': role.name,
            'permissions': json.dumps(role.permissions)
        }

    @staticmethod
    def roles_update_model_to_dict(role: RoleUpdate) -> dict:
        return {
            'name': role.name,
            'permissions': json.dumps(role.permissions)
        }

    async def add_role(self, uow: IUnitOfWork, role: RoleCreate):
        async with uow:
            role_dict = self.roles_create_model_to_dict(role)
            await self.roles_repository.add(uow.session, role_dict)
            await uow.commit()
            return role_dict['uuid']

    async def update_role(self, uow: IUnitOfWork, role_uuid: uuid.UUID, role: RoleUpdate):
        async with uow:
            role_dict = self.roles_update_model_to_dict(role)
            await self.roles_repository.edit(uow.session, role_uuid, role_dict)
            await uow.commit()
            return role_uuid

    async def delete_role(self, uow: IUnitOfWork, role_uuid: uuid.UUID):
        async with uow:
            await self.roles_repository.delete(uow.session, role_uuid)
            await uow.commit()
            return role_uuid  # нужно выпилить эту роль у всех пользователей

    async def get_fake_role(self, uow: IUnitOfWork, roles: Iterable) -> str | None:
        """
        Function that returns uuid of the first role from the given list that does not exist.
        :param roles: list of roles where a fake role is going to be found (if exists)
        :param uow: unit of work
        :return: fake role's uuid or None if it does not exist
        """
        for role_uuid in roles:
            role = await self.get_role(uow, role_uuid)
            if not role:
                return role_uuid

    async def has_permission(self, uow: IUnitOfWork, user: UserRead | UserCreate | UserUpdate, permission: str):
        for role_uuid in user.roles:
            role = await self.get_role(uow, role_uuid)
            if role and permission in role.permissions:
                return True
        return False

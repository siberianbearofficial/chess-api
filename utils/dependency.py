from typing import Annotated

from fastapi import Depends, Header

from authentication.service import AuthenticationService

from roles.repository import RolesRepository
from roles.service import RolesService

from users.repository import UsersRepository
from users.service import UsersService

from utils.unitofwork import IUnitOfWork, UnitOfWork

roles_repository = RolesRepository()
roles_service = RolesService(roles_repository)

users_repository = UsersRepository()
users_service = UsersService(users_repository)

authentication_service = AuthenticationService(users_repository)


async def get_users_service():
    return users_service


async def get_authentication_service():
    return authentication_service


async def get_roles_service():
    return roles_service


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]
RolesServiceDep = Annotated[RolesService, Depends(get_roles_service)]

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
AuthenticationDep = Annotated[str | None, Header()]

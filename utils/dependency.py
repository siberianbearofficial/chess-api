from typing import Annotated

from fastapi import Depends, Header

from authentication.service import AuthenticationService
from boards.repository import BoardsRepository
from boards.service import BoardsService
from invitations.repository import InvitationsRepository
from invitations.service import InvitationsService

from roles.repository import RolesRepository
from roles.service import RolesService

from users.repository import UsersRepository
from users.service import UsersService

from utils.unitofwork import IUnitOfWork, UnitOfWork

roles_repository = RolesRepository()
roles_service = RolesService(roles_repository)

users_repository = UsersRepository()
users_service = UsersService(users_repository)

boards_repository = BoardsRepository()
boards_service = BoardsService(boards_repository)

invitations_repository = InvitationsRepository()
invitations_service = InvitationsService(invitations_repository)

authentication_service = AuthenticationService(users_repository)


async def get_users_service():
    return users_service


async def get_authentication_service():
    return authentication_service


async def get_roles_service():
    return roles_service


async def get_boards_service():
    return boards_service


async def get_invitations_service():
    return invitations_service


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]
RolesServiceDep = Annotated[RolesService, Depends(get_roles_service)]
BoardsServiceDep = Annotated[BoardsService, Depends(get_boards_service)]
InvitationsServiceDep = Annotated[InvitationsService, Depends(get_invitations_service)]

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
AuthenticationDep = Annotated[str | None, Header()]

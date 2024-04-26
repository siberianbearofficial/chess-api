from uuid import UUID

from fastapi import APIRouter

from utils.exceptions import exception_handler
from utils.dependency import (AuthenticationServiceDep,
                              BoardsServiceDep,
                              AuthenticationDep,
                              UOWDep)

from authentication.exceptions import NotAuthenticatedError

from boards.schemas import BoardCreate, BoardUpdate
from boards.exceptions import *

router = APIRouter(prefix='/boards', tags=['Boards'])


@router.get('')
@exception_handler
async def get_boards_handler(boards_service: BoardsServiceDep,
                             authentication_service: AuthenticationServiceDep,
                             uow: UOWDep,
                             owner: UUID | None = None,
                             invited: UUID | None = None,
                             authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    boards = await boards_service.get_boards(uow, owner=owner, invited=invited)
    return {
        'data': boards,
        'detail': 'Boards were selected.'
    }


@router.get('/{uuid}')
@exception_handler
async def get_board_handler(authentication_service: AuthenticationServiceDep,
                            boards_service: BoardsServiceDep,
                            uow: UOWDep,
                            uuid: UUID,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    board = await boards_service.get_board(uow, uuid)
    if not board:
        raise BoardNotFoundError

    return {
        'data': board,
        'detail': 'Board was selected.'
    }


@router.post('')
@exception_handler
async def post_board_handler(uow: UOWDep,
                             authentication_service: AuthenticationServiceDep,
                             boards_service: BoardsServiceDep,
                             board: BoardCreate,
                             authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    uuid = await boards_service.add_board(uow, board)
    return {
        'data': str(uuid),
        'detail': 'Board was added.'
    }


@router.put('/{uuid}')
@exception_handler
async def put_board_handler(uow: UOWDep,
                            authentication_service: AuthenticationServiceDep,
                            boards_service: BoardsServiceDep,
                            uuid: UUID,
                            board: BoardUpdate,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    board_with_this_uuid = await boards_service.get_board(uow, uuid)
    if not board_with_this_uuid:
        raise BoardNotFoundError

    await boards_service.update_board(uow, uuid, board)
    return {
        'data': None,
        'detail': 'Board was updated.'
    }


@router.delete('/{uuid}')
@exception_handler
async def delete_board_handler(uow: UOWDep,
                               authentication_service: AuthenticationServiceDep,
                               boards_service: BoardsServiceDep,
                               uuid: UUID,
                               authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    board_with_this_uuid = await boards_service.get_board(uow, uuid)
    if not board_with_this_uuid:
        raise BoardNotFoundError

    await boards_service.delete_board(uow, uuid)
    return {
        'data': None,
        'detail': 'Board was deleted.'
    }

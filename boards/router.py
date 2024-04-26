from uuid import UUID

from fastapi import APIRouter

from invitations.exceptions import InvitationNotFoundError
from utils.exceptions import exception_handler
from utils.dependency import (AuthenticationServiceDep,
                              BoardsServiceDep,
                              AuthenticationDep,
                              UOWDep, InvitationsServiceDep)

from authentication.exceptions import NotAuthenticatedError

from boards.schemas import BoardCreate, BoardUpdate, BoardInvite
from boards.exceptions import *
from utils.logic import equal_uuids

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


@router.post('/{uuid}/invited')
@exception_handler
async def post_board_invited_handler(uow: UOWDep,
                                     authentication_service: AuthenticationServiceDep,
                                     boards_service: BoardsServiceDep,
                                     invitations_service: InvitationsServiceDep,
                                     invite: BoardInvite,
                                     uuid: UUID,
                                     authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    board = await boards_service.get_board(uow, uuid)
    if not board:
        raise BoardNotFoundError

    invitation = await invitations_service.get_invitation(uow, code=invite.invitation)
    if not invitation:
        raise InvitationNotFoundError

    if not equal_uuids(board.uuid, invitation.board):
        raise UpdateBoardDenied  # явно другое исключение нужно

    invited = board.invited + [invite.invited]

    uuid = await boards_service.update_board(uow, board.uuid, BoardUpdate(invited=invited))
    return {
        'data': str(uuid),
        'detail': 'Invited user was added to the board.'
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

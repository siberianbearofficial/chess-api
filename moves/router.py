from uuid import UUID

from fastapi import APIRouter

from boards.exceptions import BoardNotFoundError
from utils.exceptions import exception_handler
from utils.dependency import (AuthenticationServiceDep,
                              MovesServiceDep,
                              AuthenticationDep,
                              UOWDep, BoardsServiceDep)

from authentication.exceptions import NotAuthenticatedError

from moves.schemas import MoveCreate
from moves.exceptions import *
from utils.logic import equal_uuids

router = APIRouter(prefix='/moves', tags=['Moves'])


@router.get('')
@exception_handler
async def get_moves_handler(moves_service: MovesServiceDep,
                            authentication_service: AuthenticationServiceDep,
                            boards_service: BoardsServiceDep,
                            uow: UOWDep,
                            board: UUID | None = None,
                            actor: str | None = None,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not board:
        raise ReadMoveDenied

    b = await boards_service.get_board(uow, board)
    if not b:
        raise BoardNotFoundError

    if not equal_uuids(b.owner, author.uuid) and author.uuid not in b.invited:
        raise ReadMoveDenied

    moves = await moves_service.get_moves(uow, board=board, actor=actor)
    return {
        'data': moves,
        'detail': 'Moves were selected.'
    }


@router.get('/legal')
@exception_handler
async def get_moves_handler(moves_service: MovesServiceDep,
                            authentication_service: AuthenticationServiceDep,
                            boards_service: BoardsServiceDep,
                            uow: UOWDep,
                            board: UUID,
                            actor: str | None = None,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not board:
        raise ReadMoveDenied

    b = await boards_service.get_board(uow, board)
    if not b:
        raise BoardNotFoundError

    if not equal_uuids(b.owner, author.uuid) and author.uuid not in b.invited:
        raise ReadMoveDenied

    moves = await moves_service.get_legal_moves(uow, board_uuid=board, actor=actor)
    return {
        'data': moves,
        'detail': 'Legal moves were selected.'
    }


@router.get('/last')
@exception_handler
async def get_move_handler(authentication_service: AuthenticationServiceDep,
                           moves_service: MovesServiceDep,
                           boards_service: BoardsServiceDep,
                           uow: UOWDep,
                           board: UUID,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    b = await boards_service.get_board(uow, board)
    if not b:
        raise BoardNotFoundError

    if not equal_uuids(b.owner, author.uuid) and author.uuid not in b.invited:
        raise ReadMoveDenied

    moves = await moves_service.get_moves(uow, board=board)
    if not moves:
        raise MoveNotFoundError

    moves = sorted(moves, key=lambda m: m.created_at)

    return {
        'data': moves[-1],
        'detail': 'Move was selected.'
    }


@router.get('/{uuid}')
@exception_handler
async def get_move_handler(authentication_service: AuthenticationServiceDep,
                           moves_service: MovesServiceDep,
                           boards_service: BoardsServiceDep,
                           uow: UOWDep,
                           uuid: UUID,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    move = await moves_service.get_move(uow, uuid)
    if not move:
        raise MoveNotFoundError

    b = await boards_service.get_board(uow, move.board)
    if not b:
        raise BoardNotFoundError

    if not equal_uuids(b.owner, author.uuid) and author.uuid not in b.invited:
        raise ReadMoveDenied

    return {
        'data': move,
        'detail': 'Move was selected.'
    }


@router.post('')
@exception_handler
async def post_move_handler(uow: UOWDep,
                            authentication_service: AuthenticationServiceDep,
                            moves_service: MovesServiceDep,
                            boards_service: BoardsServiceDep,
                            move: MoveCreate,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    b = await boards_service.get_board(uow, move.board)
    if not b:
        raise BoardNotFoundError

    if not equal_uuids(b.owner, author.uuid) and author.uuid not in b.invited:
        raise InsertMoveDenied

    uuid = await moves_service.add_move(uow, move, author.uuid)
    await moves_service.clear_old_moves(uow, move.board)
    return {
        'data': str(uuid),
        'detail': 'Move was added.'
    }


@router.delete('/last')
@exception_handler
async def delete_move_handler(uow: UOWDep,
                              authentication_service: AuthenticationServiceDep,
                              moves_service: MovesServiceDep,
                              boards_service: BoardsServiceDep,
                              board: UUID,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    b = await boards_service.get_board(uow, board)
    if not b:
        raise BoardNotFoundError

    if not equal_uuids(b.owner, author.uuid) and author.uuid not in b.invited:
        raise DeleteMoveDenied

    moves = await moves_service.get_moves(uow, board=board)
    if not moves:
        raise MoveNotFoundError

    moves = sorted(moves, key=lambda m: m.created_at)

    uuid = await moves_service.undo_move(uow, moves[-1].uuid, author.uuid)
    return {
        'data': str(uuid),
        'detail': 'Move was deleted.'
    }

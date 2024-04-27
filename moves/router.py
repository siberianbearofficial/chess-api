from uuid import UUID

from fastapi import APIRouter

from utils.exceptions import exception_handler
from utils.dependency import (AuthenticationServiceDep,
                              MovesServiceDep,
                              AuthenticationDep,
                              UOWDep)

from authentication.exceptions import NotAuthenticatedError

from moves.schemas import MoveCreate, MoveUndo
from moves.exceptions import *

router = APIRouter(prefix='/moves', tags=['Moves'])


@router.get('')
@exception_handler
async def get_moves_handler(moves_service: MovesServiceDep,
                            authentication_service: AuthenticationServiceDep,
                            uow: UOWDep,
                            board: UUID | None = None,
                            actor: str | None = None,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    moves = await moves_service.get_moves(uow, board=board, actor=actor)
    return {
        'data': moves,
        'detail': 'Moves were selected.'
    }


@router.get('/{uuid}')
@exception_handler
async def get_move_handler(authentication_service: AuthenticationServiceDep,
                           moves_service: MovesServiceDep,
                           uow: UOWDep,
                           uuid: UUID,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    move = await moves_service.get_move(uow, uuid)
    if not move:
        raise MoveNotFoundError

    return {
        'data': move,
        'detail': 'Move was selected.'
    }


@router.post('')
@exception_handler
async def post_move_handler(uow: UOWDep,
                            authentication_service: AuthenticationServiceDep,
                            moves_service: MovesServiceDep,
                            move: MoveCreate,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    uuid = await moves_service.add_move(uow, move)
    return {
        'data': str(uuid),
        'detail': 'Move was added.'
    }


@router.delete('/last')
@exception_handler
async def delete_move_handler(uow: UOWDep,
                              authentication_service: AuthenticationServiceDep,
                              moves_service: MovesServiceDep,
                              move_undo: MoveUndo,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    moves = await moves_service.get_moves(uow, board=move_undo.board)
    if not moves:
        raise MoveNotFoundError

    uuid = None
    for move in sorted(moves, key=lambda m: m.created_at):
        if move.actor == move_undo.actor:
            uuid = move.uuid

    if not uuid:
        raise MoveNotFoundError  # не та ошибка, по-хорошему

    uuid = await moves_service.undo_move(uow, uuid)
    return {
        'data': str(uuid),
        'detail': 'Move was deleted.'
    }

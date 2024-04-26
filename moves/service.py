from datetime import datetime
from json import dumps
from uuid import UUID, uuid4
import chess

from utils.unitofwork import IUnitOfWork

from moves.repository import MovesRepository
from moves.schemas import MoveCreate, MoveUndo


class MovesService:
    def __init__(self, moves_repository: MovesRepository):
        self.moves_repository = moves_repository

    async def get_moves(self, uow: IUnitOfWork, board: UUID | None = None, actor: str | None = None):
        filter_by = dict()
        if board:
            filter_by['board'] = board
        if actor and actor.strip().lower() in ('white', 'black'):
            filter_by['actor'] = actor.strip().lower()
        async with uow:
            moves = await self.moves_repository.find_all(uow.session, **filter_by)
            return moves

    async def get_move(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            move = await self.moves_repository.find_one(uow.session, uuid=uuid)
            return move

    async def add_move(self, uow: IUnitOfWork, move: MoveCreate):
        async with uow:
            uuid = uuid4()
            move_dict = {
                'uuid': uuid,
                'board': move.board,
                'created_at': datetime.now(tz=None),
                'src': move.src,
                'dst': move.dst,
                'figure': 'queen'  # надо с либой разобраться и получить фигуру
            }
            if move.actor:
                move_dict['actor'] = move.actor
            else:
                move_dict['actor'] = 'white'
            await self.moves_repository.add_one(uow.session, move_dict)
            await uow.commit()
            return uuid

    # async def update_move(self, uow: IUnitOfWork, uuid: UUID, move: MoveUpdate):
    #     async with uow:
    #         move_dict = dict()
    #         if move.mode:
    #             move_dict['mode'] = move.mode
    #         if move.privacy:
    #             move_dict['privacy'] = move.privacy
    #         if move.invited:
    #             move_dict['invited'] = dumps([str(el) for el in move.invited])
    #         if move.white:
    #             move_dict['white'] = move.white
    #         if move.black:
    #             move_dict['black'] = move.black
    #         await self.moves_repository.edit_one(uow.session, uuid, move_dict)
    #         await uow.commit()
    #         return uuid

    async def delete_move(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.moves_repository.delete_one(uow.session, uuid)
            await uow.commit()
            return uuid

    # async def delete_moves(self, uow: IUnitOfWork, name: str | None = None):
    #     filter_by_dict = {'name': name} if name else {}
    #     async with uow:
    #         await self.moves_repository.delete_all(uow.session, **filter_by_dict)
    #         await uow.commit()

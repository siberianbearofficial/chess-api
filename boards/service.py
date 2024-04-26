from datetime import datetime
from json import dumps
from uuid import UUID, uuid4
import chess

from utils.unitofwork import IUnitOfWork

from boards.repository import BoardsRepository
from boards.schemas import BoardCreate, BoardUpdate


class BoardsService:
    def __init__(self, boards_repository: BoardsRepository):
        self.boards_repository = boards_repository

    async def get_boards(self, uow: IUnitOfWork, owner: UUID | None = None, invited: UUID | None = None):
        filter_by = dict()
        if owner:
            filter_by['owner'] = owner
        async with uow:
            boards = await self.boards_repository.find_all(uow.session, **filter_by)
            if invited:
                boards = list(filter(lambda board: invited in board.invited, boards))
            return boards

    async def get_board(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            board = await self.boards_repository.find_one(uow.session, uuid=uuid)
            return board

    async def add_board(self, uow: IUnitOfWork, board: BoardCreate):
        async with uow:
            uuid = uuid4()
            board_dict = {
                'uuid': uuid,
                'owner': board.owner,
                'mode': board.mode,
                'privacy': board.privacy,
                'invited': '[]',
                'white': None,
                'black': None,
                'created_at': datetime.now(tz=None),
                'status': 'created',
                'state': chess.Board().board_fen()
            }
            await self.boards_repository.add_one(uow.session, board_dict)
            await uow.commit()
            return uuid

    async def update_board(self, uow: IUnitOfWork, uuid: UUID, board: BoardUpdate):
        async with uow:
            board_dict = dict()
            if board.mode:
                board_dict['mode'] = board.mode
            if board.privacy:
                board_dict['privacy'] = board.privacy
            if board.invited:
                board_dict['invited'] = dumps([str(el) for el in board.invited])
            if board.white:
                board_dict['white'] = board.white
            if board.black:
                board_dict['black'] = board.black
            await self.boards_repository.edit_one(uow.session, uuid, board_dict)
            await uow.commit()
            return uuid

    async def delete_board(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.boards_repository.delete_one(uow.session, uuid)
            await uow.commit()

    # async def delete_boards(self, uow: IUnitOfWork, name: str | None = None):
    #     filter_by_dict = {'name': name} if name else {}
    #     async with uow:
    #         await self.boards_repository.delete_all(uow.session, **filter_by_dict)
    #         await uow.commit()

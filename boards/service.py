import json
from datetime import datetime
import uuid
import chess

from invitations.repository import InvitationsRepository
from utils.unitofwork import IUnitOfWork

from boards.repository import BoardsRepository
from boards.schemas import BoardCreate, BoardUpdate, BoardRead


class BoardsService:
    def __init__(self, boards_repository: BoardsRepository, invitations_repository: InvitationsRepository):
        self.boards_repository = boards_repository
        self.invitations_repository = invitations_repository

    async def get_boards(self, uow: IUnitOfWork,
                         owner: uuid.UUID | None = None,
                         invited: uuid.UUID | None = None,
                         as_dict: bool = False) -> list[BoardRead] | list[dict]:
        filter_by = dict()
        if owner:
            filter_by['owner'] = owner
        async with uow:
            board_dicts = await self.boards_repository.all(uow.session, **filter_by)
            if invited:
                board_dicts = list(filter(lambda board: invited in board['invited'], board_dicts))
            if as_dict:
                return board_dicts
            return [self.board_dict_to_read_model(board_dict) for board_dict in board_dicts]

    async def get_board(self, uow: IUnitOfWork, board_uuid: uuid.UUID, as_dict: bool = False) -> BoardRead | dict:
        async with uow:
            board_dict = await self.boards_repository.get(uow.session, uuid=board_uuid)
            if as_dict:
                return board_dict
            return self.board_dict_to_read_model(board_dict)

    @classmethod
    def board_dict_to_read_model(cls, board_dict: dict) -> BoardRead:
        return BoardRead(
            uuid=board_dict['uuid'],
            owner=board_dict['owner'],
            mode=board_dict['mode'],
            privacy=board_dict['privacy'],
            invited=json.loads(board_dict['invited']),
            white=board_dict['white'],
            black=board_dict['black'],
            winner=board_dict['winner'],
            created_at=board_dict['created_at'],
            status=board_dict['status'],
            state=cls.board_fen_to_dict(board_dict['state'])
        )

    @staticmethod
    def board_fen_to_dict(fen: str):
        state = dict()
        for square, piece in chess.Board(fen).piece_map().items():
            if 0 <= square < len(chess.SQUARE_NAMES):
                state[chess.SQUARE_NAMES[square]] = {
                    'figure': chess.piece_name(piece.piece_type),
                    'actor': 'white' if piece.color == chess.WHITE else 'black'
                }
        return state

    @staticmethod
    def board_create_model_to_dict(board: BoardCreate) -> dict:
        return {
            'uuid': uuid.uuid4(),
            'owner': board.owner,
            'mode': board.mode,
            'privacy': board.privacy,
            'invited': '[]',
            'white': None,
            'black': None,
            'winner': None,
            'created_at': datetime.now(tz=None),
            'status': 'created',
            'state': chess.Board().fen()
        }

    async def add_board(self, uow: IUnitOfWork, board: BoardCreate):
        async with uow:
            board_dict = self.board_create_model_to_dict(board)
            await self.boards_repository.add_one(uow.session, board_dict)
            await uow.commit()
            return board_dict['uuid']

    async def update_board(self, uow: IUnitOfWork, board_uuid: uuid.UUID, board: BoardUpdate):
        async with uow:
            board_dict = dict()
            if board.mode:
                board_dict['mode'] = board.mode
            if board.privacy:
                board_dict['privacy'] = board.privacy
            if board.invited:
                board_dict['invited'] = json.dumps([str(el) for el in board.invited])
            if board.white:
                board_dict['white'] = board.white
            if board.black:
                board_dict['black'] = board.black
            await self.boards_repository.edit_one(uow.session, board_uuid, board_dict)
            await uow.commit()
            return board_uuid

    async def delete_board(self, uow: IUnitOfWork, board_uuid: uuid.UUID):
        async with uow:
            await self.invitations_repository.delete_all(uow.session, board=board_uuid)
            await self.boards_repository.delete_one(uow.session, board_uuid)
            await uow.commit()
            return board_uuid

    # async def delete_boards(self, uow: IUnitOfWork, name: str | None = None):
    #     filter_by_dict = {'name': name} if name else {}
    #     async with uow:
    #         await self.boards_repository.delete_all(uow.session, **filter_by_dict)
    #         await uow.commit()

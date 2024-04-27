from datetime import datetime
import uuid
import chess

from boards.exceptions import BoardNotFoundError
from boards.repository import BoardsRepository
from moves.exceptions import IllegalMoveDenied
from utils.unitofwork import IUnitOfWork

from moves.repository import MovesRepository
from moves.schemas import MoveCreate, MoveRead


class MovesService:
    def __init__(self, moves_repository: MovesRepository, boards_repository: BoardsRepository):
        self.moves_repository = moves_repository
        self.boards_repository = boards_repository

    async def get_moves(self, uow: IUnitOfWork,
                        board: uuid.UUID | None = None,
                        actor: str | None = None,
                        as_dict: bool = False) -> list[MoveRead] | list[dict]:
        filter_by = dict()
        if board:
            filter_by['board'] = board
        if actor:
            filter_by['actor'] = actor.strip().lower()
        async with uow:
            move_dicts = await self.moves_repository.all(uow.session, **filter_by)
            if as_dict:
                return move_dicts
            return [self.move_dict_to_read_model(move_dict) for move_dict in move_dicts]

    async def get_move(self, uow: IUnitOfWork, move_uuid: uuid.UUID, as_dict: bool = False) -> MoveRead | dict:
        async with uow:
            move_dict = await self.moves_repository.get(uow.session, uuid=move_uuid)
            if as_dict:
                return move_dict
            return self.move_dict_to_read_model(move_dict)

    @staticmethod
    def move_dict_to_read_model(move_dict: dict) -> MoveRead:
        return MoveRead(
            uuid=move_dict.get('uuid'),
            board=move_dict.get('board'),
            actor=move_dict.get('actor'),
            created_at=move_dict.get('created_at'),
            src=move_dict.get('src'),
            dst=move_dict.get('dst'),
            figure=move_dict.get('figure')
        )

    @staticmethod
    def move_create_model_to_dict(move: MoveCreate):
        move_dict = {
            'uuid': uuid.uuid4(),
            'board': move.board,
            'created_at': datetime.now(tz=None),
            'src': move.src,
            'dst': move.dst
        }
        return move_dict

    async def add_move(self, uow: IUnitOfWork, move: MoveCreate):
        async with uow:
            board_dict = await self.boards_repository.get(uow.session, uuid=move.board)
            if not board_dict:
                raise BoardNotFoundError
            prev_state = board_dict['state']

            board = chess.Board(prev_state)

            try:
                board.push_uci(f'{move.src}{move.dst}')  # в этот момент все отвалится, если был передан невалидный ход
            except chess.IllegalMoveError | chess.InvalidMoveError | chess.AmbiguousMoveError:
                raise IllegalMoveDenied

            board_dict['state'] = board.fen()
            outcome = board.outcome()
            if outcome:
                board_dict['status'] = outcome.termination.name.lower()
                if outcome.winner is None:
                    board_dict['winner'] = None
                elif outcome.winner:
                    board_dict['winner'] = 'white'
                else:
                    board_dict['winner'] = 'black'
            elif board.is_check():
                board_dict['status'] = 'check'
                board_dict['winner'] = None
            await self.boards_repository.edit_one(uow.session, move.board, board_dict)
            move_dict = self.move_create_model_to_dict(move)
            move_dict['board_prev_state'] = prev_state
            dst_square = chess.SQUARE_NAMES.index(move.dst)
            if move.actor:
                move_dict['actor'] = move.actor
            else:
                move_dict['actor'] = 'white' if board.color_at(dst_square) else 'black'
            dst_piece = board.piece_at(dst_square)
            move_dict['figure'] = chess.PIECE_NAMES[0 if not dst_piece else dst_piece.piece_type]
            await self.moves_repository.add_one(uow.session, move_dict)

            await uow.commit()
            return move_dict['uuid']

    async def clear_old_moves(self, uow: IUnitOfWork, board_uuid: uuid.UUID):
        pass

    async def undo_move(self, uow: IUnitOfWork, move_uuid: uuid.UUID):
        async with uow:
            move_dict = await self.moves_repository.get(uow.session, uuid=move_uuid)
            board_dict = await self.boards_repository.get(uow.session, uuid=move_dict['board'])
            board_dict['state'] = move_dict['board_prev_state']

            board = chess.Board(board_dict['state'])
            outcome = board.outcome()
            if outcome:
                board_dict['status'] = outcome.termination.name.lower()
                if outcome.winner is None:
                    board_dict['winner'] = None
                elif outcome.winner:
                    board_dict['winner'] = 'white'
                else:
                    board_dict['winner'] = 'black'
            elif board.is_check():
                board_dict['winner'] = None
                board_dict['status'] = 'check'
            else:
                board_dict['winner'] = None
                board_dict['status'] = 'created'

            await self.boards_repository.edit_one(uow.session, board_dict['uuid'], board_dict)
            await self.moves_repository.delete_one(uow.session, move_uuid)
            await uow.commit()
            return move_uuid

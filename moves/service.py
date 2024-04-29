from datetime import datetime
import uuid
import chess.svg
import chess

from boards.exceptions import BoardNotFoundError
from boards.repository import BoardsRepository
from moves.exceptions import IllegalMoveDenied
from utils.unitofwork import IUnitOfWork

from moves.repository import MovesRepository
from moves.schemas import MoveCreate, MoveRead, LegalMove


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
            move_dicts = await self.moves_repository.get_all(uow.session, **filter_by)
            if as_dict:
                return move_dicts
            return [self.moves_dict_to_read_model(move_dict) for move_dict in move_dicts]

    async def get_move(self, uow: IUnitOfWork, move_uuid: uuid.UUID, as_dict: bool = False) -> MoveRead | dict | None:
        async with uow:
            move_dict = await self.moves_repository.get(uow.session, uuid=move_uuid)
            if not move_dict:
                return None
            if as_dict:
                return move_dict
            return self.moves_dict_to_read_model(move_dict)

    async def get_legal_moves(self, uow: IUnitOfWork,
                              board_uuid: uuid.UUID,
                              actor: str | None = None) -> list[LegalMove]:
        async with uow:
            board_dict = await self.boards_repository.get(uow.session, uuid=board_uuid)
            board = chess.Board(board_dict['state'])
            moves = list()
            for move in board.legal_moves:
                moves.append(LegalMove(
                    board=board_uuid,
                    actor=actor or ('white' if board.color_at(move.from_square) else 'black'),
                    src=chess.square_name(move.from_square),
                    dst=chess.square_name(move.to_square),
                    figure=chess.piece_name(board.piece_at(move.from_square).piece_type),
                    promotion=None if (move.promotion is None) else chess.piece_name(move.promotion)
                ))
            return moves

    @staticmethod
    def moves_dict_to_read_model(move_dict: dict) -> MoveRead:
        return MoveRead(
            uuid=move_dict.get('uuid'),
            board=move_dict.get('board'),
            actor=move_dict.get('actor'),
            created_at=move_dict.get('created_at'),
            src=move_dict.get('src'),
            dst=move_dict.get('dst'),
            figure=move_dict.get('figure'),
            promotion=move_dict.get('promotion')
        )

    @staticmethod
    def moves_create_model_to_dict(move: MoveCreate):
        return {
            'uuid': uuid.uuid4(),
            'board': move.board,
            'created_at': datetime.now(tz=None),
            'src': move.src,
            'dst': move.dst,
            'promotion': move.promotion
        }

    async def add_move(self, uow: IUnitOfWork, move: MoveCreate, illegal_allowed: bool = False):
        async with (uow):
            board_dict = await self.boards_repository.get(uow.session, uuid=move.board)
            if not board_dict:
                raise BoardNotFoundError

            prev_state = board_dict['state']
            board = chess.Board(prev_state)
            print(board.unicode())
            try:
                uci = self.get_move_uci(move)
                print(repr(uci))
                board.push_uci(uci)
            except:
                raise IllegalMoveDenied

            board_dict['state'] = board.fen()
            board_dict['status'], board_dict['winner'] = self.get_board_status_and_winner(board)
            await self.boards_repository.edit(uow.session, move.board, board_dict)

            move_dict = self.moves_create_model_to_dict(move)
            move_dict['board_prev_state'] = prev_state
            move_dict['actor'] = self.get_move_actor(board, move, illegal_allowed)
            move_dict['figure'] = self.get_move_figure(board, move)
            await self.moves_repository.add(uow.session, move_dict)

            await uow.commit()
            return move_dict['uuid']

    @staticmethod
    def get_move_uci(move: MoveCreate | MoveRead | LegalMove):
        if move.promotion is None:
            return f'{move.src}{move.dst}'
        promotion = chess.piece_symbol(chess.PIECE_NAMES.index(move.promotion))
        return f'{move.src}{move.dst}{promotion}'

    @staticmethod
    def get_move_figure(board: chess.Board, move: MoveCreate | MoveRead | LegalMove):
        dst_piece = board.piece_at(chess.parse_square(move.dst))
        if not dst_piece:
            return None
        return chess.piece_name(dst_piece.piece_type)

    @classmethod
    def get_move_actor(cls, board: chess.Board, move: MoveCreate | MoveRead | LegalMove, illegal_allowed: bool = False):
        actor_from_lib = cls._color_name(board.color_at(chess.parse_square(move.dst)))
        print(repr(actor_from_lib))
        print(repr(move.actor))
        if move.actor:
            if illegal_allowed or move.actor == actor_from_lib:
                return move.actor
            raise IllegalMoveDenied  # другая ошибка, по-хорошему
        return actor_from_lib

    @classmethod
    def get_board_status_and_winner(cls, board: chess.Board | str):
        if isinstance(board, str):
            board = chess.Board(board)

        if board.is_variant_loss():
            return 'variant_loss', cls._color_name(not board.turn)
        if board.is_variant_win():
            return 'variant_win', cls._color_name(board.turn)
        if board.is_variant_draw():
            return 'variant_draw', None

        if board.is_checkmate():
            return 'checkmate', cls._color_name(not board.turn)
        if board.is_insufficient_material():
            return 'insufficient_material', None
        if not any(board.generate_legal_moves()):
            return 'stalemate', None

        if board.is_seventyfive_moves():
            return 'seventyfive_moves', None
        if board.is_fivefold_repetition():
            return 'fivefold_repetition', None

        if board.is_check():
            return 'check', None

        if board.fen() != chess.STARTING_FEN:
            return 'progress', None

        return 'created', None

    @staticmethod
    def _color_name(color: chess.Color) -> str | None:
        if color == chess.WHITE:
            return 'white'
        if color == chess.BLACK:
            return 'black'
        return None

    async def clear_old_moves(self, uow: IUnitOfWork, board_uuid: uuid.UUID):
        pass

    async def undo_move(self, uow: IUnitOfWork, move_uuid: uuid.UUID):
        async with uow:
            move_dict = await self.moves_repository.get(uow.session, uuid=move_uuid)

            board_dict = await self.boards_repository.get(uow.session, uuid=move_dict['board'])
            board_dict['state'] = move_dict['board_prev_state']
            board_dict['status'], board_dict['winner'] = self.get_board_status_and_winner(board_dict['state'])

            await self.boards_repository.edit(uow.session, board_dict['uuid'], board_dict)
            await self.moves_repository.delete(uow.session, move_uuid)
            await uow.commit()
            return move_uuid

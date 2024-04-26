from utils.repository import SQLAlchemyRepository

from boards.models import Board


class BoardsRepository(SQLAlchemyRepository):
    model = Board

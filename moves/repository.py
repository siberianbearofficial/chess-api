from utils.repository import SQLAlchemyRepository

from moves.models import Move


class MovesRepository(SQLAlchemyRepository):
    model = Move

from utils.repository import SQLAlchemyRepository

from users.models import User


class UsersRepository(SQLAlchemyRepository):
    model = User

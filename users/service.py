from uuid import UUID

from users.model import UserCreate


class UserService:
    def __init__(self, repository: UserRepository = None):
        self.repository = repository

    async def get_users_alg(self, id: UUID) -> UserAlg:
        users_alg = await self.repository.find_one(uuid=id)
        return users_alg

    async def get_users_algs(self) -> list[UserAlg]:
        users_algs = await self.repository.find_all()
        print('Users algs were selected:', users_algs)
        return users_algs

    async def create_user(self, user_create: UserCreate):
        users_alg = await self.get_users_alg(user_create.alg_id)
        if not users_alg:
            return None
        user = await users_alg.solve(user_create.params)
        print('User was created.')
        return user

from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.repository import SQLAlchemyRepository

from invitations.models import Invitation


class InvitationsRepository(SQLAlchemyRepository):
    model = Invitation

    async def add(self, session: AsyncSession, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.code)
        res = await session.execute(stmt)
        return res.scalar_one()

    async def edit(self, session: AsyncSession, code: str, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(code=code).returning(self.model.code)
        res = await session.execute(stmt)
        return res.scalar_one()

    async def delete(self, session, code: str):
        stmt = delete(self.model).where(self.model.code == code).returning(self.model.code)
        res = await session.execute(stmt)
        return res

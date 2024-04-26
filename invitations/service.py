from datetime import datetime
from uuid import UUID, uuid4

from utils.unitofwork import IUnitOfWork

from invitations.repository import InvitationsRepository
from invitations.schemas import InvitationCreate


class InvitationsService:
    def __init__(self, invitations_repository: InvitationsRepository):
        self.invitations_repository = invitations_repository

    async def get_invitations(self, uow: IUnitOfWork, board: UUID | None = None):
        filter_by = dict()
        if board:
            filter_by['board'] = board
        async with uow:
            invitations = await self.invitations_repository.find_all(uow.session, **filter_by)
            return invitations

    async def get_invitation(self, uow: IUnitOfWork, code: str):
        async with uow:
            invitation = await self.invitations_repository.find_one(uow.session, code=code)
            return invitation

    async def add_invitation(self, uow: IUnitOfWork, invitation: InvitationCreate):
        async with uow:
            code = await self.__generate_invitation_code()
            invitation_dict = {
                'code': code,
                'board': invitation.board,
                'created_at': datetime.now(tz=None)
            }
            await self.invitations_repository.add_one(uow.session, invitation_dict)
            await uow.commit()
            return code

    @staticmethod
    async def __generate_invitation_code():
        return str(uuid4()).replace('-', '')[:6]

    async def delete_invitation(self, uow: IUnitOfWork, code: str):
        async with uow:
            await self.invitations_repository.delete_one(uow.session, code)
            await uow.commit()
            return code

    # async def delete_invitations(self, uow: IUnitOfWork, name: str | None = None):
    #     filter_by_dict = {'name': name} if name else {}
    #     async with uow:
    #         await self.invitations_repository.delete_all(uow.session, **filter_by_dict)
    #         await uow.commit()

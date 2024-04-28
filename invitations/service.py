from datetime import datetime
from uuid import UUID, uuid4

from utils.unitofwork import IUnitOfWork

from invitations.repository import InvitationsRepository
from invitations.schemas import InvitationCreate, InvitationRead


class InvitationsService:
    def __init__(self, invitations_repository: InvitationsRepository):
        self.invitations_repository = invitations_repository

    async def get_invitations(self, uow: IUnitOfWork,
                              board: UUID | None = None,
                              as_dict: bool = False) -> list[InvitationRead] | list[dict]:
        filter_by = dict()
        if board:
            filter_by['board'] = board
        async with uow:
            invitations_dict = await self.invitations_repository.get_all(uow.session, **filter_by)
            if as_dict:
                return invitations_dict
            return [self.invitations_dict_to_read_model(invitation) for invitation in invitations_dict]

    async def get_invitation(self, uow: IUnitOfWork, code: str, as_dict: bool = False) -> InvitationRead | dict | None:
        async with uow:
            invitation_dict = await self.invitations_repository.get(uow.session, code=code)
            if not invitation_dict:
                return None
            if as_dict:
                return invitation_dict
            return self.invitations_dict_to_read_model(invitation_dict)

    @staticmethod
    def invitations_dict_to_read_model(invitation: dict) -> InvitationRead:
        return InvitationRead(
            code=invitation['code'],
            board=invitation['board'],
            created_at=invitation['created_at']
        )

    @classmethod
    def invitations_create_model_to_dict(cls, invitation: InvitationCreate) -> dict:
        return {
            'code': cls.__generate_invitation_code(),
            'board': invitation.board,
            'created_at': datetime.now(tz=None)
        }

    async def add_invitation(self, uow: IUnitOfWork, invitation: InvitationCreate):
        async with uow:
            invitation_dict = self.invitations_create_model_to_dict(invitation)
            await self.invitations_repository.add(uow.session, invitation_dict)
            await uow.commit()
            return invitation_dict['code']

    @staticmethod
    def __generate_invitation_code():
        return str(uuid4()).replace('-', '')[:6]

    async def delete_invitation(self, uow: IUnitOfWork, code: str):
        async with uow:
            await self.invitations_repository.delete(uow.session, code)
            await uow.commit()
            return code

    # async def delete_invitations(self, uow: IUnitOfWork, name: str | None = None):
    #     filter_by_dict = {'name': name} if name else {}
    #     async with uow:
    #         await self.invitations_repository.delete_all(uow.session, **filter_by_dict)
    #         await uow.commit()

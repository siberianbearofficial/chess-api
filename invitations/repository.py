from utils.repository import SQLAlchemyRepository

from invitations.models import Invitation


class InvitationsRepository(SQLAlchemyRepository):
    model = Invitation

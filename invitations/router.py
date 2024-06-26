from uuid import UUID

from fastapi import APIRouter

from utils.exceptions import exception_handler
from utils.dependency import (AuthenticationServiceDep,
                              InvitationsServiceDep,
                              AuthenticationDep,
                              UOWDep)

from authentication.exceptions import NotAuthenticatedError

from invitations.schemas import InvitationCreate
from invitations.exceptions import *

router = APIRouter(prefix='/invitations', tags=['Invitations'])


@router.get('')
@exception_handler
async def get_invitations_handler(invitations_service: InvitationsServiceDep,
                                  authentication_service: AuthenticationServiceDep,
                                  uow: UOWDep,
                                  board: UUID | None = None,
                                  authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    invitations = await invitations_service.get_invitations(uow, board=board)
    return {
        'data': invitations,
        'detail': 'Invitations were selected.'
    }


@router.get('/{code}')
@exception_handler
async def get_invitation_handler(authentication_service: AuthenticationServiceDep,
                                 invitations_service: InvitationsServiceDep,
                                 uow: UOWDep,
                                 code: str,
                                 authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    invitation = await invitations_service.get_invitation(uow, code)
    if not invitation:
        raise InvitationNotFoundError

    return {
        'data': invitation,
        'detail': 'Invitation was selected.'
    }


@router.post('')
@exception_handler
async def post_invitation_handler(uow: UOWDep,
                                  authentication_service: AuthenticationServiceDep,
                                  invitations_service: InvitationsServiceDep,
                                  invitation: InvitationCreate,
                                  authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    code = await invitations_service.add_invitation(uow, invitation)
    return {
        'data': code,
        'detail': 'Invitation was added.'
    }


@router.delete('/{code}')
@exception_handler
async def delete_invitation_handler(uow: UOWDep,
                                    authentication_service: AuthenticationServiceDep,
                                    invitations_service: InvitationsServiceDep,
                                    code: str,
                                    authorization: AuthenticationDep = None):
    author = await authentication_service.authenticated_user(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    invitation_with_this_uuid = await invitations_service.get_invitation(uow, code)
    if not invitation_with_this_uuid:
        raise InvitationNotFoundError

    await invitations_service.delete_invitation(uow, code)
    return {
        'data': None,
        'detail': 'Invitation was deleted.'
    }

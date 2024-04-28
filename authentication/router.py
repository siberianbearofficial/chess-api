from fastapi import APIRouter

from utils.exceptions import exception_handler
from utils.dependency import UOWDep, AuthenticationServiceDep

from authentication.schemas import AuthenticationCreate

router = APIRouter(prefix='/authentication', tags=['Authentication'])


@router.post('')
@exception_handler
async def post_sign_in_handler(authentication_service: AuthenticationServiceDep,
                               uow: UOWDep,
                               authentication: AuthenticationCreate):
    data = await authentication_service.authenticate(uow, authentication)
    return {
        'data': data,
        'detail': 'Authenticated successfully.'
    }

from typing import Annotated

from fastapi import Depends, Header

from solutions.repository import SolutionRepository
from solutions.service import SolutionService

# from utils.unitofwork import IUnitOfWork, UnitOfWork

solutions_repository = SolutionRepository()
solutions_service = SolutionService(solutions_repository)


async def get_solutions_service():
    return solutions_service


SolutionServiceDep = Annotated[SolutionService, Depends(get_solutions_service)]

# UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
AuthenticationDep = Annotated[str | None, Header()]

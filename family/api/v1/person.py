from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from family.services.persons import PersonService
from family.utils.container import Container

# from family.adapters.schemas.persons import PersonAnswer

person = APIRouter(prefix="/persons", tags=["Persons"])


@person.get(
    "/{person_id}",
    summary="Info about person",
    # response_model=PersonAnswer,
)
@inject
async def person_info(
    person_id: str,
    service: PersonService = Depends(Provide[Container.person_service]),
):
    return await service.info(person_id)

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from family.adapters.schemas.persons import PersonAnswer, PersonFamily
from family.services.persons import PersonService
from family.utils.container import Container

person = APIRouter(prefix="/persons", tags=["Persons"])


@person.get(
    "/{person_id}",
    summary="Info about person",
    response_model=PersonAnswer,
)
@inject
async def person_info(
    person_id: str,
    service: PersonService = Depends(Provide[Container.person_service]),
):
    return await service.info(person_id)


@person.get("/{person_id}/family", summary="Family spose", response_model=PersonFamily)
@inject
async def person_family_spose(
    person_id: str,
    service: PersonService = Depends(Provide[Container.person_service]),
):
    return await service.person_with_family(person_id)

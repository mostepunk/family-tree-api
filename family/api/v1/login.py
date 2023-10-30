from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from family.adapters.schemas.accounts import AccountSchema
from family.api.dependencies import create_token, get_user_from_token
from family.services.accounts import AccountService
from family.utils.container import Container

login = APIRouter(prefix="/accounts", tags=["accounts"])


@login.post("/login", summary="login user")
@inject
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AccountService = Depends(Provide[Container.account_service]),
):
    user = await service.authentiacate_user(form_data.username, form_data.password)
    return {"access_token": await create_token(user), "token_type": "bearer"}


@login.get("/refresh-token", summary="Обновить токен без аутентификации")
async def refresh_token(account: Annotated[get_user_from_token, Depends()]):
    return {"access_token": await create_token(account), "token_type": "bearer"}


@login.get(
    "/me",
    summary="information about authorised user",
    response_model=AccountSchema,
)
async def about_me(account: Annotated[get_user_from_token, Depends()]):
    return account


@login.get("/token", summary="токен в виде строки", response_model=str)
async def token_str(
    request: Request, account: Annotated[get_user_from_token, Depends()]
):
    return request.headers.get("authorization").lstrip("Bearer ")

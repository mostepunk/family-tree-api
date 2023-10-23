from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from family.api.dependencies import create_token, get_user_from_token
from family.services.accounts import AccountService, AccountUOW

login = APIRouter(tags=["accounts"])


@login.post("/login", summary="login user")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    service = AccountService(AccountUOW())
    user = await service.authentiacate_user(form_data.username, form_data.password)
    return {"access_token": await create_token(user), "token_type": "bearer"}


@login.get("/refresh-token", summary="Обновить токен без аутентификации")
async def refresh_token(account: Annotated[get_user_from_token, Depends()]):
    service = AccountService(AccountUOW())
    return {"access_token": await create_token(user), "token_type": "bearer"}

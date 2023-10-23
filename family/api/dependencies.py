from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, SecurityScopes
from jwt import DecodeError
from loguru import logger as logging
from pydantic import ValidationError

from family.adapters.schemas.accounts import AccountDBSchema, AccountSchema, Roles
from family.adapters.schemas.token import Token
from family.resources.timezones import MOSCOW
from family.settings import Environment, app_settings, jwt_settings, oauth2_scheme

security = HTTPBearer()


async def create_token(
    account: AccountDBSchema,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = Token(
        username=account.username, email=account.email, roles=account.roles
    )
    to_encode.exp = datetime.now(tz=MOSCOW) + timedelta(
        minutes=expires_delta or jwt_settings.token_expire
    )

    encoded_jwt: str = jwt.encode(
        to_encode.dict(), jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALG
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Извлечь данные из токена"""

    try:
        return jwt.decode(
            token,
            algorithms=jwt_settings.ALG,
            key=jwt_settings.SECRET_KEY,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
            },
        )
    except DecodeError as err:
        raise HTTPException(
            status_code=401, detail=f"Invalid JWT token with error {err}"
        ) from err


async def get_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> AccountSchema:
    """Получение пользователя из токена"""
    if app_settings.app_env == Environment.local:
        return AccountSchema(
            uuid=uuid4(),
            username="root",
            email="root@domain.com",
            roles=[Roles.superadmin],
        )

    try:
        account = AccountSchema.parse_obj(decode_token(token))
    except ValidationError:
        logging.error(f"Invalid schema from token. schema = {decode_token(token)}")
        raise HTTPException(status_code=403, detail="Invalid user schema from token")
    except Exception as exc:
        logging.error(f"{exc}")
        raise HTTPException(status_code=403, detail="Invalid token")
    else:
        return account


async def check_roles(
    security_scopes: SecurityScopes,
    account: AccountSchema = Depends(get_user_from_token),
):
    """Декоратор для проверки прав"""
    if app_settings.app_env == Environment.local:
        return
    if account.is_superadmin():
        return
    if not account.has_access(security_scopes):
        raise HTTPException(status_code=403, detail="Forbidden: Not enough rights")

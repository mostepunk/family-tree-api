from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, SecurityScopes
from jwt import DecodeError
from pydantic import ValidationError
from starlette.requests import Request

# from app.schemas.users import User
# from app.settings import AppEnvTypes, app_settings, db_settings, jwt_settings
# from app.utils.logger import logger


SECRET_KEY = jwt_settings.SECRET
ALG = jwt_settings.ALG

security = HTTPBearer()


def decode_token(token: str) -> dict:
    """Извлечь данные из токена"""

    try:
        return jwt.decode(
            token,
            algorithms=ALG,
            key=SECRET_KEY,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
            },
        )
    except DecodeError as e:
        raise HTTPException(status_code=401, detail=f"Invalid JWT token with error {e}")


async def get_user_from_token(request: Request) -> User:
    """Получение пользователя из токена"""
    token: str = request.headers.get("x-user-token")
    if app_settings.app_env == AppEnvTypes.local:
        return User(
            uuid=uuid4(),
            username="Суперадмин",
            email="capex_superadmin@example.com",
            roles=["LIVING.REQUEST_TRACKER.ROLE.ALL_ACCESS"],
        )
    if not token:
        raise HTTPException(status_code=403, detail="Forbidden: Not enough token")
    try:
        user = User.parse_obj(decode_token(token))
        return user
    except ValidationError:
        logger.error(f"Invalid schema from token. schema = {decode_token(token)}")
        raise HTTPException(status_code=403, detail="Invalid user schema from token")
    except Exception as exc:
        logger.error(f"{exc}")
        raise HTTPException(status_code=403, detail="Invalid token")


async def check_roles(
    security_scopes: SecurityScopes, user: User = Depends(get_user_from_token)
):
    """Декоратор для проверки прав"""
    if app_settings.app_env == AppEnvTypes.local:
        return
    if user.is_superadmin():
        return
    if not user.has_access(security_scopes):
        raise HTTPException(status_code=403, detail="Forbidden: Not enough rights")

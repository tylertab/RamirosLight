from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import User
from app.schemas.user import UserRead

from .config import SettingsSingleton
from .singleton import SingletonMeta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/accounts/login")
optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/accounts/login", auto_error=False
)


class PasswordHasher(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)


class TokenService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._settings = SettingsSingleton().instance

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> tuple[str, datetime]:
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + (
            expires_delta or timedelta(minutes=self._settings.access_token_expire_minutes)
        )
        to_encode.update({"exp": int(expire.timestamp())})
        token = jwt.encode(to_encode, self._settings.secret_key, algorithm="HS256")
        return token, expire


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    settings = SettingsSingleton().instance
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        subject = payload.get("sub")
        if subject is None:
            raise ValueError("Missing subject")
        user_id = int(subject)
    except (JWTError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return UserRead.model_validate(user)


async def get_optional_user(
    token: str | None = Depends(optional_oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserRead | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SettingsSingleton().instance.secret_key, algorithms=["HS256"])
        subject = payload.get("sub")
        if subject is None:
            return None
        user_id = int(subject)
    except (JWTError, ValueError):
        return None

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return UserRead.model_validate(user) if user else None

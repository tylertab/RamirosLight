from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.user import UserRead

from .config import SettingsSingleton
from .singleton import SingletonMeta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/accounts/login")


class PasswordHasher(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)


class TokenService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._settings = SettingsSingleton().instance

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + (
            expires_delta or timedelta(minutes=self._settings.access_token_expire_minutes)
        )
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, self._settings.secret_key, algorithm="HS256")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRead:
    settings = SettingsSingleton().instance
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return UserRead(**payload["sub"])
    except (JWTError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

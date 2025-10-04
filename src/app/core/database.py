from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Base

from .config import SettingsSingleton
from .singleton import ResettableSingletonMeta, SingletonMeta


class DatabaseSessionManager(metaclass=ResettableSingletonMeta):
    def __init__(self) -> None:
        settings = SettingsSingleton().instance

        if settings.database_url.startswith("sqlite"):
            db_path = settings.database_url.split("///")[-1]
            if db_path and db_path != ":memory:":
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self._engine = create_async_engine(settings.database_url, echo=False, future=True)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    @property
    def engine(self):  # type: ignore[override]
        return self._engine

    def session(self) -> AsyncSession:
        return self._session_factory()


async def init_models() -> None:
    settings = SettingsSingleton().instance
    if settings.database_url.startswith("sqlite"):
        # sqlite needs to ensure directory exists
        db_path = settings.database_url.split("///")[-1]
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    async with DatabaseSessionManager().engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = DatabaseSessionManager().session()
    try:
        yield session
    finally:
        await session.close()

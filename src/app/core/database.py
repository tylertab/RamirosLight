from collections.abc import AsyncGenerator
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

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


class DatabaseSchemaManager:
    def __init__(self, engine: AsyncEngine | None = None) -> None:
        self._engine = engine or DatabaseSessionManager().engine

    async def ensure_schema(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.run_sync(self._ensure_user_subscription_columns)
            await conn.run_sync(self._ensure_federation_submission_columns)

    def _ensure_user_subscription_columns(self, sync_conn) -> None:
        if sync_conn.dialect.name != "sqlite":
            return
        inspector = sa.inspect(sync_conn)
        if "users" not in inspector.get_table_names():
            return
        existing_columns = {column["name"] for column in inspector.get_columns("users")}
        required_columns = {
            "subscription_tier": "TEXT NOT NULL DEFAULT 'FREE'",
            "subscription_expires_at": "TIMESTAMP",
            "subscription_started_at": "TIMESTAMP",
            "subscription_renewal_period_days": "INTEGER NOT NULL DEFAULT 30",
            "last_payment_reference": "VARCHAR(120)",
        }
        for column_name, ddl in required_columns.items():
            if column_name not in existing_columns:
                sync_conn.execute(sa.text(f"ALTER TABLE users ADD COLUMN {column_name} {ddl}"))

    def _ensure_federation_submission_columns(self, sync_conn) -> None:
        if sync_conn.dialect.name != "sqlite":
            return

        inspector = sa.inspect(sync_conn)
        if "federation_submissions" not in inspector.get_table_names():
            return

        existing_columns = {
            column["name"] for column in inspector.get_columns("federation_submissions")
        }

        required_columns = {
            "status_details": "VARCHAR(500)",
            "processed_at": "TIMESTAMP",
            "verified_at": "TIMESTAMP",
            "checksum": "VARCHAR(128)",
        }

        for column_name, ddl in required_columns.items():
            if column_name not in existing_columns:
                sync_conn.execute(
                    sa.text(f"ALTER TABLE federation_submissions ADD COLUMN {column_name} {ddl}")
                )


async def init_models() -> None:
    settings = SettingsSingleton().instance
    if settings.database_url.startswith("sqlite"):
        # sqlite needs to ensure directory exists
        db_path = settings.database_url.split("///")[-1]
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    await DatabaseSchemaManager().ensure_schema()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = DatabaseSessionManager().session()
    try:
        yield session
    finally:
        await session.close()

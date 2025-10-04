from __future__ import annotations

from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class SQLAlchemyRepository(Generic[ModelType]):
    """Lightweight repository wrapper around an ``AsyncSession``.

    The repository centralizes common query helpers which keeps the service
    layer focused on business logic and avoids error-prone hand written SQL in
    multiple places.
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self._session = session
        self._model = model

    @property
    def model(self) -> type[ModelType]:
        return self._model

    async def get(self, object_id: int) -> ModelType | None:
        stmt = select(self._model).where(self._model.id == object_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self) -> Sequence[ModelType]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def get_by(self, column: InstrumentedAttribute, value: object) -> ModelType | None:
        stmt = select(self._model).where(column == value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, instance: ModelType) -> ModelType:
        self._session.add(instance)
        await self._session.flush()
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self._session.delete(instance)

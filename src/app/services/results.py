"""Helpers for querying recent competition results."""

from __future__ import annotations

from sqlalchemy import Select, desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Event, EventDiscipline, EventEntry
from app.schemas.result import ResultSummary


class ResultsService:
    """Query helpers to surface lightweight result summaries."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_recent(self, limit: int = 10) -> list[ResultSummary]:
        """Return the latest updated entries with their discipline and event context."""

        stmt = self._base_query().order_by(desc(EventEntry.updated_at)).limit(limit)
        result = await self._session.execute(stmt)
        return [self._build_summary(row) for row in result.all()]

    async def search(self, query: str, limit: int = 10) -> list[ResultSummary]:
        """Search recent results across athlete, team, discipline, and event fields."""

        pattern = f"%{query}%"
        stmt = (
            self._base_query()
            .where(
                or_(
                    EventEntry.athlete_name.ilike(pattern),
                    EventEntry.team_name.ilike(pattern),
                    EventEntry.result.ilike(pattern),
                    EventDiscipline.name.ilike(pattern),
                    Event.name.ilike(pattern),
                    Event.location.ilike(pattern),
                )
            )
            .order_by(desc(EventEntry.updated_at))
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [self._build_summary(row) for row in result.all()]

    def _base_query(self) -> Select[tuple[EventEntry, EventDiscipline, Event]]:
        return (
            select(EventEntry, EventDiscipline, Event)
            .join(EventDiscipline, EventDiscipline.id == EventEntry.discipline_id)
            .join(Event, Event.id == EventDiscipline.event_id)
        )

    @staticmethod
    def _build_summary(row: tuple[EventEntry, EventDiscipline, Event]) -> ResultSummary:
        entry, discipline, event = row
        return ResultSummary(
            entry_id=entry.id,
            event_id=event.id,
            event_name=event.name,
            event_location=event.location,
            discipline_id=discipline.id,
            discipline_name=discipline.name,
            discipline_round=discipline.round_name,
            athlete_name=entry.athlete_name,
            team_name=entry.team_name,
            position=entry.position,
            result=entry.result,
            updated_at=entry.updated_at,
        )

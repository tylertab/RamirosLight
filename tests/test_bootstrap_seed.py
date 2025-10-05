import pytest
from sqlalchemy import select

from app.core.config import SettingsSingleton
from app.core.database import DatabaseSessionManager, init_models
from app.models import Event, NewsArticle, Roster, User
from app.services.bootstrap import seed_initial_data


@pytest.mark.anyio("asyncio")
async def test_seed_initial_data_populates_demo_records(tmp_path, monkeypatch):
    db_path = tmp_path / "seed_demo.db"
    monkeypatch.setenv("ATHLETICS_DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")
    monkeypatch.setenv("ATHLETICS_SEED_DEMO_DATA", "true")

    SettingsSingleton.reset_instance()
    DatabaseSessionManager.reset_instance()

    await init_models()
    await seed_initial_data()

    session = DatabaseSessionManager().session()
    try:
        counts = {}
        for model in (User, Event, Roster, NewsArticle):
            result = await session.execute(select(model))
            counts[model.__name__] = len(result.scalars().all())
    finally:
        await session.close()
        DatabaseSessionManager.reset_instance()
        SettingsSingleton.reset_instance()

    assert counts["Event"] >= 3
    assert counts["Roster"] >= 3
    assert counts["NewsArticle"] >= 3

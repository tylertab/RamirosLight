import sqlite3

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


@pytest.mark.anyio("asyncio")
async def test_init_models_adds_ingest_token_hash_column(tmp_path, monkeypatch):
    db_path = tmp_path / "missing_ingest.db"
    monkeypatch.setenv("ATHLETICS_DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE federations (
                id INTEGER PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                country VARCHAR(80),
                website VARCHAR(255)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

    SettingsSingleton.reset_instance()
    DatabaseSessionManager.reset_instance()

    await init_models()

    DatabaseSessionManager.reset_instance()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("PRAGMA table_info('federations')")
        columns = {row[1] for row in cursor.fetchall()}
    finally:
        conn.close()
        DatabaseSessionManager.reset_instance()
        SettingsSingleton.reset_instance()

    assert "ingest_token_hash" in columns


@pytest.mark.anyio("asyncio")
async def test_init_models_adds_roster_club_id_column(tmp_path, monkeypatch):
    db_path = tmp_path / "missing_club_id.db"
    monkeypatch.setenv("ATHLETICS_DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE rosters (
                id INTEGER PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                country VARCHAR(80),
                division VARCHAR(80),
                coach_name VARCHAR(120),
                athlete_count INTEGER
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

    SettingsSingleton.reset_instance()
    DatabaseSessionManager.reset_instance()

    await init_models()

    DatabaseSessionManager.reset_instance()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("PRAGMA table_info('rosters')")
        columns = {row[1] for row in cursor.fetchall()}
    finally:
        conn.close()
        DatabaseSessionManager.reset_instance()
        SettingsSingleton.reset_instance()

    assert "club_id" in columns

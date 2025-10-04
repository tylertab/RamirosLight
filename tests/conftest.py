import asyncio
import os
import sys
from pathlib import Path

import pytest
from httpx import AsyncClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app.core.config import SettingsSingleton  # noqa: E402
from app.core.database import DatabaseSessionManager, init_models  # noqa: E402
from main import create_app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def configure_settings(tmp_path_factory: pytest.TempPathFactory):
    db_path = tmp_path_factory.mktemp("db") / "test_app.db"
    os.environ["ATHLETICS_DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"
    os.environ["ATHLETICS_SEED_DEMO_DATA"] = "false"
    SettingsSingleton.reset_instance()
    DatabaseSessionManager.reset_instance()
    asyncio.run(init_models())
    yield
    DatabaseSessionManager.reset_instance()
    SettingsSingleton.reset_instance()
    os.environ.pop("ATHLETICS_SEED_DEMO_DATA", None)
    if Path(db_path).exists():
        Path(db_path).unlink()


@pytest.fixture
def app(configure_settings):
    return create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

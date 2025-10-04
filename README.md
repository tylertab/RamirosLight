# Pan-American Athletics Hub Backend

A modular FastAPI backend that powers a South America-wide athletics portal. The project favors free-tier friendly services, singleton-managed infrastructure, and clear standard operating procedures (SOPs) to make onboarding simple.

## Features
- Async FastAPI API with versioned routers for accounts, events, federations, and health checks.
- SQLAlchemy ORM models with SQLite (dev) and Postgres-ready configuration for free cloud databases.
- Singleton-based configuration, database session factory, password hashing, and message bus.
- Federation ingestion pipeline stub backed by an in-process queue.
- Comprehensive SOPs covering development, deployment, data ingestion, and operations.

## Getting Started
1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Bootstrap the database**
   > The project uses a `src/` layout, so either export `PYTHONPATH=src` once per shell session or prefix commands that import `app.*` modules.
   ```bash
   PYTHONPATH=src python -c "import asyncio; from app.core.database import init_models; asyncio.run(init_models())"
   ```
3. **Run the API**
   ```bash
   uvicorn src.main:app --reload
   ```
4. **Explore the docs** – visit `http://localhost:8000/docs` for interactive OpenAPI docs.

## Environment Variables
Configure via `.env` (all optional defaults provided):

| Variable | Purpose | Default |
| --- | --- | --- |
| `ATHLETICS_PROJECT_NAME` | Service name | `Pan-American Athletics Hub` |
| `ATHLETICS_ENVIRONMENT` | Environment label | `development` |
| `ATHLETICS_DATABASE_URL` | SQLAlchemy database URL | `sqlite+aiosqlite:///./data/app.db` |
| `ATHLETICS_REDIS_URL` | Redis connection (future use) | `redis://localhost:6379/0` |
| `ATHLETICS_SECRET_KEY` | JWT signing secret | `change-me` |
| `ATHLETICS_ALLOWED_HOSTS` | Comma-separated hosts | `*` |

## Tests
Tests are not yet implemented. Suggested next steps include adding pytest-based API and service tests and wiring them into CI.

## Documentation & SOPs
- [Architecture](docs/architecture.md)
- SOPs located in the [`sop/`](sop) directory.

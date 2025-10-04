# Pan-American Athletics Hub Backend

A modular FastAPI backend that powers a South America-wide athletics portal. The project favors free-tier friendly services, singleton-managed infrastructure, and clear standard operating procedures (SOPs) to make onboarding simple.

## Features
- Async FastAPI API with versioned routers for accounts, events, federations, search, subscriptions, and health checks.
- Server-rendered multi-page web portal (home, profiles, events, rosters, federations upload, auth, about) served from `src/app/web/templates` with a shared base layout.
- Locale-aware front-end powered by `static/app.js`, featuring an English, Spanish, and Portuguese translation dictionary, navigation actions, and authenticated federation upload workflows.
- SQLAlchemy ORM models with SQLite (dev) and Postgres-ready configuration for free cloud databases.
- Singleton-based configuration, database session factory, password hashing, and message bus used across services.
- Federation ingestion pipeline stub backed by an in-process queue with secure upload management through the web experience.
- Comprehensive SOPs covering development, deployment, data ingestion, and operations.

## Prerequisites
- Python 3.11 or 3.12 (3.13 is not yet supported because of upstream dependency constraints.)
- Git

## Getting Started
1. **Run the quick setup script** – automates virtualenv creation, dependency installation, `.env` generation, static asset linking, and database bootstrapping. Override defaults with `PYTHON_BIN`, `VENV_PATH`, or `REQUIREMENTS_FILE` as needed.
   ```bash
   ./scripts/dev_setup.sh
   ```
2. **Activate the virtual environment** (the script creates `.venv` by default)
   ```bash
   source .venv/bin/activate
   export PYTHONPATH=$(pwd)/src
   ```
3. **Run the API + web portal**
   ```bash
   uvicorn src.main:app --reload
   ```
4. **Explore the web portal** – visit `http://localhost:8000/` for the localized multi-page UI (language selector is located in the footer and persists per session).
5. **Review the API docs** – visit `http://localhost:8000/docs` for interactive OpenAPI documentation.

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
Run the full suite with:

```bash
pytest
```

The tests exercise authentication, subscription upgrades, content search, and federation ingestion flows to ensure the web interactions backed by the API remain stable.

## Documentation & SOPs
- [Architecture](docs/architecture.md)
- SOPs located in the [`sop/`](sop) directory.

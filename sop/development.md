# Development SOP

## 1. Prerequisites
- Python 3.11 or 3.12 (we currently cap at <3.13 until dependencies add support)
- Git
- (Optional) SQLite CLI for inspecting the local database.
- (Optional) Modern browser for exercising the web portal (Chrome/Edge/Firefox).

## 2. Environment Setup
1. Clone the repository.
2. Run the bootstrap script (idempotent) – this provisions `.venv`, installs dependencies, wires static assets, creates `.env`, and initializes the SQLite database:
   ```bash
   ./scripts/dev_setup.sh
   ```
   Override defaults with environment variables (`PYTHON_BIN`, `VENV_PATH`, `REQUIREMENTS_FILE`) when necessary.
3. If you prefer manual setup, create a virtualenv, `pip install -r requirements.txt`, create `.env`, and initialize the database with:
   ```bash
   PYTHONPATH=src python -c "import asyncio; from app.core.database import init_models; asyncio.run(init_models())"
   ```

## 3. Running Services Locally
- Launch API + web portal with `uvicorn src.main:app --reload`.
- Visit `http://localhost:8000/` to interact with the localized multi-page UI.
- Optional: run Redis locally via Docker `docker run -p 6379:6379 redis:alpine` once caching is introduced.

## 4. Coding Standards
- Follow PEP 8 and type annotate all new modules.
- Organize new features into `schemas`, `models`, `services`, and `api` routers.
- Reuse singleton-managed dependencies instead of instantiating resources directly.
- Add docstrings for public methods/classes.
- Web templates should extend `base.html`; wire new navigation items through the `nav` section and map page-specific strings into the translation dictionary in `static/app.js`.
- Page behaviors in `static/app.js` should check `pageId` to avoid leaking logic across views.

## 5. Testing
- Run `pytest` before committing. The suite covers authentication, subscription upgrades, search, and federation ingestion workflows.
- New integration tests should use `httpx.AsyncClient` fixtures under `tests/` to align with existing patterns.
- Extend or update front-end tests by instrumenting view-specific API interactions via the Python tests (UI relies on API behavior).

## 6. Git Workflow
1. Create a feature branch from `main`.
2. Commit atomic changes with descriptive messages.
3. Open a PR, ensuring lint/test checks pass (GitHub Actions to be configured).
4. Request review from a project maintainer.

## 7. Documentation
- Update `docs/architecture.md` when architectural decisions change.
- Add or modify SOPs if a new repeatable process is established.

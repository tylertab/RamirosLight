# Development SOP

## 1. Prerequisites
- Python 3.11+
- Git
- (Optional) SQLite CLI for inspecting the local database.

## 2. Environment Setup
1. Clone the repository and create a Python virtual environment.
2. Install dependencies via `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` (or create `.env`) if you need to override defaults.
4. Initialize the database:
   ```bash
   python -c "import asyncio; from app.core.database import init_models; asyncio.run(init_models())"
   ```

## 3. Running Services Locally
- Launch API with `uvicorn src.main:app --reload`.
- Optional: run Redis locally via Docker `docker run -p 6379:6379 redis:alpine` once caching is introduced.

## 4. Coding Standards
- Follow PEP 8 and type annotate all new modules.
- Organize new features into `schemas`, `models`, `services`, and `api` routers.
- Reuse singleton-managed dependencies instead of instantiating resources directly.
- Add docstrings for public methods/classes.

## 5. Testing
- Add pytest suites under `tests/` (to be created) for services and API endpoints.
- Use `httpx.AsyncClient` for FastAPI integration tests.
- Ensure new tests pass locally before opening a PR.

## 6. Git Workflow
1. Create a feature branch from `main`.
2. Commit atomic changes with descriptive messages.
3. Open a PR, ensuring lint/test checks pass (GitHub Actions to be configured).
4. Request review from a project maintainer.

## 7. Documentation
- Update `docs/architecture.md` when architectural decisions change.
- Add or modify SOPs if a new repeatable process is established.

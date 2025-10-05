# Deployment SOP

## Overview
Deploy the FastAPI + server-rendered portal to a free-tier platform. These instructions assume [Railway](https://railway.app/) but translate directly to Render or Fly.io. The application boots via `uvicorn`, auto-creates tables, and seeds demo data when the environment variable `ATHLETICS_SEED_DEMO_DATA` (default `True`) is set.

## 1. Prerequisites
- GitHub repository up to date on `main`.
- Railway account linked to GitHub.
- Neon (or equivalent Postgres provider) project with credentials.
- Optional: Better Stack account for centralized logs + uptime.

Before provisioning, run the local checks:

```bash
./scripts/dev_setup.sh  # ensures dependencies + migrations succeed locally
pytest                   # run automated tests
```

If your environment blocks outbound PyPI traffic, configure `PIP_INDEX_URL`/`PIP_EXTRA_INDEX_URL` before invoking the setup script.

## 2. Prepare Environment Variables
Create a `.env.production` file locally based on `.env.example` and populate secrets. Required keys:

| Variable | Description | Example |
| --- | --- | --- |
| `ATHLETICS_PROJECT_NAME` | Display name for the app | `Pan-American Athletics Hub` |
| `ATHLETICS_ENVIRONMENT` | Environment label | `production` |
| `ATHLETICS_DATABASE_URL` | SQLAlchemy async URL | `postgresql+asyncpg://<user>:<pwd>@<host>/<db>` |
| `ATHLETICS_SECRET_KEY` | JWT signing key | `generate-long-random-value` |
| `ATHLETICS_ALLOWED_HOSTS` | Comma-separated hostnames | `your-subdomain.up.railway.app` |
| `ATHLETICS_REDIS_URL` | (Optional) external Redis | `rediss://...` |
| `ATHLETICS_SEED_DEMO_DATA` | Disable demo seeding in prod | `false` |

> **Note:** The project uses the `asyncpg` driver. Ensure `requirements.txt` is synced in Railway so Nixpacks installs `asyncpg` during the build.

## 3. Provision the Railway Service
1. In Railway, **New Project → Deploy from GitHub Repo**, pick this repository.
2. Set the service to use the Python environment (Railway auto-detects with Nixpacks).
3. Under **Variables**, paste the values from your production env file.
4. Override the generated commands:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Trigger the first deploy and monitor build logs. Expect `uvicorn` to start listening on the provided port.

## 4. Database Setup with Neon
1. Create a free Postgres branch + database in Neon.
2. From the Neon dashboard, copy the connection string and convert to SQLAlchemy async format by replacing the prefix with `postgresql+asyncpg://`.
3. Update the Railway `ATHLETICS_DATABASE_URL` variable with this async URL. Include `sslmode=require` query parameter if mandated by the provider.
4. From the Railway project shell run schema initialization (FastAPI also runs this on boot, but doing it manually surfaces issues early):

   ```bash
   railway run "PYTHONPATH=src python -c 'import asyncio; from app.core.database import init_models; asyncio.run(init_models())'"
   ```

5. (Optional) Seed production-safe data by invoking `app.services.bootstrap.seed_initial_data` with `ATHLETICS_SEED_DEMO_DATA=false` to avoid demo entries.

## 5. Continuous Deployment
- Enable auto-deploy on push to `main` (or a dedicated `deploy` branch) in Railway settings.
- Protect the branch with CI checks: `pytest`, linting, security scan (e.g., `pip-audit`).
- Document environment changes in the repository (`sop/deployment.md`) when variables or commands evolve.

## 6. Post-Deployment Verification
After each deploy:
- Visit `https://<railway-app>.up.railway.app/` and navigate home → profiles → events → federations upload to verify template rendering + localization.
- Call `GET /api/v1/health` to ensure the service is healthy.
- Exercise authentication: register (`/api/v1/accounts/register`), log in (`/login`), and confirm token issuance allows `/federations/upload` submissions.
- Inspect Neon to confirm new users/events persist.

## 7. Rollback Procedure
- Use Railway **Deployments → Redeploy** on the last known good build.
- If configuration drift is suspected, restore previous env variable values via **Variables → History**.
- Communicate the incident + mitigation steps following the Operations SOP.

## 8. Monitoring & Alerts
- Stream Railway logs to [Better Stack Logs](https://betterstack.com/logs) for retention.
- Configure uptime probes (Better Stack Uptime or UptimeRobot) hitting `/api/v1/health` every minute.
- Set Neon connection alerts for connection spikes or CPU limits.


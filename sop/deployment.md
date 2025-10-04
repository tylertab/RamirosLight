# Deployment SOP

## Overview
This SOP outlines how to deploy the FastAPI service onto a free-tier platform. Instructions assume you use Railway, but Render/Fly.io follow similar steps.

## 1. Prerequisites
- GitHub repository with latest code pushed to `main`.
- Railway account (free tier) linked to GitHub.

## 2. Initial Provisioning
1. Sign in to [Railway](https://railway.app/).
2. Create a new project and select **Deploy from GitHub repo**.
3. Choose the repository hosting this backend.
4. On the service setup page, specify:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11 (set via Railway's Nixpacks or add `railway.toml`).
5. Add environment variables from `.env.example` under the project settings.
6. Deploy and monitor build logs.

## 3. Database Setup (Neon)
1. Create a free account at [Neon](https://console.neon.tech/).
2. Provision a Postgres database and note the connection string.
3. Update Railway environment variable `ATHLETICS_DATABASE_URL` with the Neon connection string (use `postgresql+psycopg_async://` driver, install `psycopg[binary]`).
4. Run migrations/initialization (Railway shells need `PYTHONPATH=src` to resolve the `app.*` modules):
   ```bash
   railway run "PYTHONPATH=src python -c 'import asyncio; from app.core.database import init_models; asyncio.run(init_models())'"
   ```

## 4. Continuous Deployment
- Enable Railway's auto-deploy on push to `main` or a dedicated `deploy` branch.
- Protect the branch with required status checks (tests, lint).

## 5. Post-Deployment Verification
- Hit `/api/v1/health` to verify readiness.
- Create a test user using `/api/v1/accounts/register`.
- Confirm database entries via Neon dashboard.

## 6. Rollback Procedure
- Railway retains previous deploys. Use the **Deployments** tab to redeploy the last known good version.
- Alternatively, redeploy a specific git commit.

## 7. Monitoring & Alerts
- Connect Railway logs to [Better Stack Logs](https://betterstack.com/logs) for persisted logging.
- Configure uptime monitoring using [Better Stack Uptime](https://betterstack.com/uptime) or [UptimeRobot](https://uptimerobot.com/).


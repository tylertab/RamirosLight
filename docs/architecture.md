# Pan-American Athletics Hub – Architecture Overview

## Goals
- Provide a lightweight, modular backend capable of supporting a continent-wide athletics community.
- Avoid paid infrastructure by leaning on reputable free-tier services.
- Embrace the singleton pattern for shared dependencies (configuration, database, cache, message bus) to keep modules decoupled.

## High-Level Components
| Layer | Description |
| --- | --- |
| API | FastAPI application exposing versioned JSON endpoints for accounts, events, federations, and health checks. |
| Services | Business logic classes (`AccountsService`, `EventsService`, `FederationIngestionService`) instantiated per-request but backed by singleton-managed infrastructure. |
| Data | Async SQLAlchemy models persisted in a PostgreSQL-compatible database (local SQLite in development). |
| Messaging | Lightweight in-process `MessageBus` enabling federation submission workflows without an external broker during prototyping. |
| Integrations | Pluggable connectors for caches, email, analytics, etc. (stubs provided for future expansion). |

## Infrastructure Choices (Free/Low-Cost)
- **Application Hosting:** [Railway](https://railway.app/), [Render](https://render.com/), [Fly.io](https://fly.io/) free tiers for containerized FastAPI deployment.
- **Database:** [Neon](https://neon.tech/) or [Supabase](https://supabase.com/) free Postgres instances. SQLite is bundled for local prototyping.
- **Caching/Queues:** [Upstash Redis](https://upstash.com/) free tier; can replace in-process `MessageBus` once ready.
- **Storage:** [Cloudflare R2](https://www.cloudflare.com/products/r2/) or [Supabase Storage] free quotas for media assets.
- **Static Frontend:** [Vercel](https://vercel.com/) or [Netlify](https://www.netlify.com/) free tiers for SPAs.
- **Monitoring:** [Better Stack Logs](https://betterstack.com/logs) free tier, [Grafana Cloud](https://grafana.com/products/cloud/) free metrics.
- **CI/CD:** GitHub Actions (free for public repos) running formatting, tests, and security scans.

## Data Model Summary
- `users`: core identities with roles (fan, athlete, coach, scout, federation, admin).
- `federations`: directory of validated organizing bodies linked to events.
- `events`: metadata describing meets, location, start/end dates, and associated federations.
- `federation_submissions`: queue of ingestion payloads with status tracking.

## Security Considerations
- Passwords hashed with bcrypt via `passlib` singleton.
- Environment-aware configuration managed through `SettingsSingleton` to avoid hard-coding secrets.
- JWT scaffolding prepared in `TokenService` for future authentication flows.
- CORS, rate limiting, and 2FA to be added as modules are implemented.

## Extensibility Roadmap
1. Implement authentication endpoints (login, refresh tokens, password reset).
2. Add role-based access control middleware.
3. Integrate external queue (Upstash/Kafka) and storage for ingestion payloads.
4. Expand schema coverage: performances, leaderboards, media, news.
5. Create Next.js frontend consuming API endpoints.
6. Harden observability with OpenTelemetry exporters.


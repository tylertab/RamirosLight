# Operations SOP

## 1. Daily Checks
- Review uptime dashboard (Better Stack or UptimeRobot) for incidents.
- Scan Railway logs for errors or elevated response times.
- Confirm federation submissions processed in the last 24 hours; follow up on failures.

## 2. Incident Response
1. **Triage**: Determine scope (API down, ingestion stalled, auth failures).
2. **Mitigation**: Roll back via Railway deployment history or disable problematic feature flag.
3. **Communication**: Notify stakeholders via email/Slack with status and ETA.
4. **Resolution**: Implement fix, deploy, and verify using `/api/v1/health` and regression tests.
5. **Postmortem**: Document cause, remediation, and action items in shared Notion/Google Doc within 48 hours.

## 3. Backup & Recovery
- Neon provides point-in-time restore (free tier retains 7 days). Schedule weekly exports to Supabase Storage via cron job.
- For local SQLite development, backup `data/app.db` before destructive schema changes.

## 4. Security Hygiene
- Rotate `ATHLETICS_SECRET_KEY` every 90 days; update JWT tokens accordingly.
- Enforce MFA on GitHub and Railway accounts.
- Review dependency updates monthly using `pip-audit` (add to CI).

## 5. Performance Monitoring
- Enable FastAPI middleware to log request duration (future task).
- Integrate Grafana Cloud free tier for metrics using [Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator).
- Set alert thresholds: P95 latency > 1.5s, error rate > 1% for 5 minutes.

## 6. Capacity Planning
- Track user growth monthly; if concurrency exceeds free-tier limits, plan migration to paid tiers.
- Evaluate queue throughput; migrate from in-process queue to Upstash Redis once daily submissions exceed 100.

## 7. Change Management
- Use GitHub Projects to track features/bugs.
- Require at least one peer review before merging.
- Maintain changelog summarizing releases and operational impacts.


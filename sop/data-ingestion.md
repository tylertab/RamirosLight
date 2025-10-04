# Federation Data Ingestion SOP

## Objective
Standardize how South American track & field federations submit race results and roster updates while using only free-tier infrastructure during the pilot phase.

## 1. Submission Channels
- **REST API** (`POST /api/v1/federations/submissions`): Preferred for automated feeds.
- **Signed URL Uploads:** Federations upload CSV/JSON to shared storage (Supabase Storage bucket). Provide signed URL in the API payload.
- **Manual Upload Form:** Future enhancement using the frontend portal.

## 2. Payload Specification
```json
{
  "federation_name": "Confederación Atlética Argentina",
  "contact_email": "data@cda.org.ar",
  "payload_url": "https://storage.supabase.co/.../results.csv",
  "notes": "Preliminary results for Nacional U20"
}
```

## 3. Validation Checklist
1. Verify `payload_url` domain is whitelisted (Supabase, Google Drive with signed link, Dropbox).
2. Ensure file format is CSV or JSON; reject others.
3. Confirm `contact_email` matches registered federation account.

## 4. Processing Workflow
1. API stores submission in `federation_submissions` table with status `queued`.
2. `MessageBus` publishes event `federation.submission` with submission ID.
3. Background worker (future Celery/RQ task) pulls payload, validates schema, and normalizes units.
4. Persist cleaned results to `performances` tables and update leaderboards.
5. Set submission status to `processed` or `failed` with diagnostic notes.

## 5. Manual Intervention
- Operations team monitors new submissions via admin dashboard (to be built).
- If validation fails, contact federation via provided email with error report.
- Use shared Google Sheet to track resolution during pilot stage.

## 6. Storage Strategy (Free Tier)
- Create Supabase project (free) dedicated bucket `federation-results` with object expiry after 30 days.
- Restrict access using row-level policies; only signed URLs accepted by API.

## 7. Data Retention & Compliance
- Delete raw uploads after 90 days or once processed.
- Maintain normalized results indefinitely for historical analytics.
- Ensure compliance with Brazil's LGPD by honoring takedown requests within 30 days.


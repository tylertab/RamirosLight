import asyncio
from uuid import uuid4

import pytest

pytestmark = pytest.mark.anyio("asyncio")


async def test_federation_submission_uses_ingest_token(client):
    unique = uuid4().hex[:6]
    federation_payload = {
        "email": f"fed_{unique}@example.com",
        "full_name": "Federation Admin",
        "role": "federation",
        "password": "SecurePass123",
    }

    register_response = await client.post("/api/v1/accounts/register", json=federation_payload)
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/accounts/login",
        data={"username": federation_payload["email"], "password": federation_payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    submission_payload = {
        "federation_name": "Confederación Andina de Atletismo",
        "contact_email": f"fed_{unique}@example.com",
        "payload_url": "https://data.trackeo.test/results.json",
        "notes": "Day 1 finals",
        "access_token": "caa-demo-token",
    }

    accepted_response = await client.post(
        "/api/v1/federations/submissions",
        json=submission_payload,
    )
    assert accepted_response.status_code == 202
    submission_body = accepted_response.json()
    assert submission_body["status"] == "queued"

    await asyncio.sleep(0.1)

    headers = {"Authorization": f"Bearer {token}"}
    list_response = await client.get("/api/v1/federations/submissions", headers=headers)
    assert list_response.status_code == 200
    submissions = list_response.json()
    assert submissions
    processed = submissions[0]
    assert processed["status"] in {"processed", "processing", "queued"}

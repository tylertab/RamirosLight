from uuid import uuid4

import pytest

pytestmark = pytest.mark.anyio("asyncio")


async def test_registration_and_login_returns_token(client):
    unique = uuid4().hex[:6]
    payload = {
        "email": f"fan_{unique}@example.com",
        "full_name": "Trackeo Fan",
        "role": "fan",
        "password": "SuperSecure123",
    }

    register_response = await client.post("/api/v1/accounts/register", json=payload)
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/accounts/login",
        data={"username": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body and body["access_token"]
    assert "expires_at" in body


async def test_public_history_access_is_free(client):
    unique = uuid4().hex[:6]
    athlete_payload = {
        "email": f"history_{unique}@example.com",
        "full_name": "History Athlete",
        "role": "athlete",
        "password": "History123!",
    }

    register_response = await client.post("/api/v1/accounts/register", json=athlete_payload)
    assert register_response.status_code == 201
    athlete_id = register_response.json()["id"]

    history_response = await client.get(f"/api/v1/athletes/{athlete_id}/history")
    assert history_response.status_code == 200
    body = history_response.json()
    assert body["athlete_id"] == athlete_id

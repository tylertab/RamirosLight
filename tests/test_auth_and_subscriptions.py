import pytest

from uuid import uuid4

from app.domain import SubscriptionTier


pytestmark = pytest.mark.anyio("asyncio")


async def test_auth_flow_and_subscription_upgrade(client):
    unique = uuid4().hex[:6]
    athlete_payload = {
        "email": f"athlete_{unique}@example.com",
        "full_name": "Test Athlete",
        "role": "athlete",
        "password": "SecurePass123",
    }
    coach_payload = {
        "email": f"coach_{unique}@example.com",
        "full_name": "Coach User",
        "role": "coach",
        "password": "SecurePass123",
    }

    athlete_response = await client.post("/api/v1/accounts/register", json=athlete_payload)
    assert athlete_response.status_code == 201
    athlete_id = athlete_response.json()["id"]

    coach_response = await client.post("/api/v1/accounts/register", json=coach_payload)
    assert coach_response.status_code == 201

    login_response = await client.post(
        "/api/v1/accounts/login",
        data={"username": coach_payload["email"], "password": coach_payload["password"]},
    )
    assert login_response.status_code == 200
    token_body = login_response.json()
    assert token_body["subscription_tier"] == SubscriptionTier.FREE.value
    token = token_body["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    history_response = await client.get(f"/api/v1/athletes/{athlete_id}/history", headers=headers)
    assert history_response.status_code == 402

    upgrade_response = await client.post(
        "/api/v1/subscriptions/upgrade",
        json={"tier": SubscriptionTier.COACH.value, "duration_days": 60},
        headers=headers,
    )
    assert upgrade_response.status_code == 200
    upgraded = upgrade_response.json()
    assert upgraded["tier"] == SubscriptionTier.COACH.value

    history_response = await client.get(f"/api/v1/athletes/{athlete_id}/history", headers=headers)
    assert history_response.status_code == 200
    history_body = history_response.json()
    assert history_body["athlete_id"] == athlete_id
    assert any(entry["event"].startswith("Trackeo") for entry in history_body["history"])

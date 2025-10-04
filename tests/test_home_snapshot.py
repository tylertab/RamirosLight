import pytest
from uuid import uuid4

from app.domain import SubscriptionTier

pytestmark = pytest.mark.anyio("asyncio")


async def test_bootstrap_home_endpoint_returns_data(client):
    unique = uuid4().hex[:6]
    coach_payload = {
        "email": f"coach_{unique}@example.com",
        "full_name": "Coach Snapshot",
        "role": "coach",
        "password": "Snapshot123",
    }
    athlete_payload = {
        "email": f"athlete_{unique}@example.com",
        "full_name": "Athlete Snapshot",
        "role": "athlete",
        "password": "Snapshot123",
    }
    event_payload = {
        "name": f"Snapshot Invitational {unique}",
        "location": "La Paz, Bolivia",
        "start_date": "2025-06-05",
        "end_date": "2025-06-07",
        "federation_id": None,
    }
    roster_payload = {
        "name": f"Snapshot Club {unique}",
        "country": "Bolivia",
        "division": "Senior",
        "coach_name": "Maria Snapshot",
        "athlete_count": 12,
    }
    news_payload = {
        "title": f"Snapshot Club {unique} sets relay record",
        "region": "La Paz",
        "excerpt": "Highlights from the Snapshot Invitational.",
        "content": "Relay squads clocked national records at the Snapshot Invitational.",
        "audience": "public",
    }

    await client.post("/api/v1/accounts/register", json=coach_payload)
    await client.post("/api/v1/accounts/register", json=athlete_payload)

    login_response = await client.post(
        "/api/v1/accounts/login",
        data={"username": coach_payload["email"], "password": coach_payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    upgrade_response = await client.post(
        "/api/v1/subscriptions/upgrade",
        json={"tier": SubscriptionTier.COACH.value, "duration_days": 60},
        headers=headers,
    )
    assert upgrade_response.status_code == 200

    event_response = await client.post("/api/v1/events/", json=event_payload)
    assert event_response.status_code == 201
    event_id = event_response.json()["id"]

    demo_response = await client.post(
        f"/api/v1/events/{event_id}/demo",
        json={
            "start_time": "2025-06-05T14:00:00Z",
            "sessions": 2,
            "disciplines_per_session": 2,
            "lanes": 4,
            "include_results": True,
        },
    )
    assert demo_response.status_code == 200

    roster_response = await client.post("/api/v1/rosters/", json=roster_payload, headers=headers)
    assert roster_response.status_code == 201

    news_response = await client.post("/api/v1/news/", json=news_payload, headers=headers)
    assert news_response.status_code == 201

    response = await client.get("/api/v1/bootstrap/home")
    assert response.status_code == 200
    data = response.json()

    assert any(user["email"] == athlete_payload["email"] for user in data["athletes"])
    assert any(event["id"] == event_id for event in data["events"])
    assert any(roster["name"] == roster_payload["name"] for roster in data["rosters"])
    assert any(article["title"] == news_payload["title"] for article in data["news"])
    assert data["live_event"]
    assert data["live_event"]["disciplines"]


async def test_templates_embed_initial_data(client):
    home_response = await client.get("/")
    assert home_response.status_code == 200
    assert 'id="initial-home-data"' in home_response.text

    event_response = await client.get("/events/9999")
    assert event_response.status_code == 200
    assert 'id="initial-event-data"' in event_response.text

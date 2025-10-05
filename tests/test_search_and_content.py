import pytest

from uuid import uuid4

from app.core.database import DatabaseSessionManager
from app.domain import SubscriptionTier
from app.models import Federation


pytestmark = pytest.mark.anyio("asyncio")


async def test_search_returns_multi_category_results(client):
    unique = uuid4().hex[:6]
    session = DatabaseSessionManager().session()
    federation = Federation(
        name=f"Andean Athletics Federation {unique}",
        country="Chile",
        website="https://andina.example.com",
    )
    session.add(federation)
    await session.commit()
    await session.refresh(federation)
    await session.close()

    coach_payload = {
        "email": f"searchcoach_{unique}@example.com",
        "full_name": "Search Coach",
        "role": "coach",
        "password": "SecurePass123",
    }
    athlete_payload = {
        "email": f"searchathlete_{unique}@example.com",
        "full_name": "Club Runner",
        "role": "athlete",
        "password": "SecurePass123",
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

    await client.post(
        "/api/v1/subscriptions/upgrade",
        json={"tier": SubscriptionTier.COACH.value, "duration_days": 90},
        headers=headers,
    )

    event_response = await client.post(
        "/api/v1/events/",
        json={
            "name": f"Andean Championship {unique}",
            "location": "Sao Paulo",
            "start_date": "2025-05-01",
            "end_date": "2025-05-02",
            "federation_id": federation.id,
        },
    )
    assert event_response.status_code == 201
    event_id = event_response.json()["id"]
    await client.post(
        f"/api/v1/events/{event_id}/demo",
        json={
            "start_time": "2025-05-01T14:00:00Z",
            "sessions": 1,
            "disciplines_per_session": 2,
            "lanes": 4,
            "include_results": True,
        },
    )

    await client.post(
        "/api/v1/rosters/",
        json={
            "name": f"Club Andean Condor {unique}",
            "country": "Chile",
            "division": "Senior",
            "coach_name": "Ana Morales",
            "athlete_count": 15,
        },
        headers=headers,
    )

    await client.post(
        "/api/v1/news/",
        json={
            "title": f"Andean relay squad {unique} secures victory",
            "region": "Santiago",
            "excerpt": "Dominant performance in regional finals.",
            "content": "Full race analysis for premium subscribers.",
            "audience": "premium",
        },
        headers=headers,
    )

    search_response = await client.get(
        "/api/v1/search/",
        params={
            "query": "Andean",
            "categories": ["events", "federations", "clubs", "news", "results"],
        },
        headers=headers,
    )
    assert search_response.status_code == 200
    results = search_response.json()["results"]
    categories = {result["category"] for result in results}
    assert {"Events", "Federations", "Clubs", "News", "Results"}.issubset(categories)
    assert any(item["title"].startswith("Andean Championship") for item in results if item["category"] == "Events")
    assert any("Andean Athletics Federation" in item["title"] for item in results if item["category"] == "Federations")
    assert any("Club Andean" in item["title"] for item in results if item["category"] == "Clubs")
    assert any("Andean relay" in item["title"] for item in results if item["category"] == "News")
    assert any("Andean Championship" in item.get("subtitle", "") for item in results if item["category"] == "Results")


async def test_detail_endpoints_surface_linked_data(client):
    unique = uuid4().hex[:6]
    athlete_payload = {
        "email": f"detail_athlete_{unique}@example.com",
        "full_name": "Detail Athlete",
        "role": "athlete",
        "password": "DetailPass123",
    }

    register_response = await client.post("/api/v1/accounts/register", json=athlete_payload)
    assert register_response.status_code == 201
    athlete = register_response.json()

    login_response = await client.post(
        "/api/v1/accounts/login",
        data={"username": athlete_payload["email"], "password": athlete_payload["password"]},
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

    roster_payload = {
        "name": f"Detail Club {unique}",
        "country": "Argentina",
        "division": "Senior",
        "coach_name": "Lucia Perez",
        "athlete_count": 8,
    }
    roster_response = await client.post("/api/v1/rosters/", json=roster_payload, headers=headers)
    assert roster_response.status_code == 201
    roster = roster_response.json()

    athlete_detail_response = await client.get(f"/api/v1/athletes/{athlete['id']}")
    assert athlete_detail_response.status_code == 200
    athlete_detail = athlete_detail_response.json()
    assert athlete_detail["full_name"] == athlete_payload["full_name"]
    assert any(item["id"] == roster["id"] for item in athlete_detail.get("rosters", []))

    roster_detail_response = await client.get(f"/api/v1/rosters/{roster['id']}")
    assert roster_detail_response.status_code == 200
    roster_detail = roster_detail_response.json()
    assert roster_detail["owner"]["full_name"] == athlete_payload["full_name"]
    assert any(item["id"] == athlete["id"] for item in roster_detail.get("athletes", []))

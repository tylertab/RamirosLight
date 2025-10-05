import pytest

from uuid import uuid4

from app.domain import SubscriptionTier


pytestmark = pytest.mark.anyio("asyncio")


async def test_search_returns_multi_category_results(client):
    unique = uuid4().hex[:6]
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

    await client.post(
        "/api/v1/events/",
        json={
            "name": f"Club Championship {unique}",
            "location": "Sao Paulo",
            "start_date": "2025-05-01",
            "end_date": "2025-05-02",
            "federation_id": None,
        },
    )

    await client.post(
        "/api/v1/rosters/",
        json={
            "name": f"Club Condor {unique}",
            "country": "Chile",
            "division": "Senior",
            "coach_name": "Ana Morales",
            "athlete_count": 15,
            "club": {
                "name": f"Condor Athletics {unique}",
                "city": "Santiago",
                "country": "Chile",
                "federation_id": None,
            },
        },
        headers=headers,
    )

    await client.post(
        "/api/v1/news/",
        json={
            "title": f"Club Condor {unique} secures relay victory",
            "region": "Santiago",
            "excerpt": "Dominant performance in regional finals.",
            "content": "Full race analysis for premium subscribers.",
            "audience": "premium",
        },
        headers=headers,
    )

    search_response = await client.get(
        "/api/v1/search/",
        params={"query": "Club", "categories": ["athletes", "events", "rosters", "news"]},
        headers=headers,
    )
    assert search_response.status_code == 200
    results = search_response.json()["results"]
    categories = {result["category"] for result in results}
    assert {"Athletes", "Events", "Rosters", "News"}.issubset(categories)


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
        "club": {
            "name": f"River Plate Track {unique}",
            "city": "Buenos Aires",
            "country": "Argentina",
            "federation_id": None,
        },
    }
    roster_response = await client.post("/api/v1/rosters/", json=roster_payload, headers=headers)
    assert roster_response.status_code == 201
    roster = roster_response.json()
    assert roster["club"]["name"] == roster_payload["club"]["name"]
    assert roster["federation"] is None

    athlete_detail_response = await client.get(f"/api/v1/athletes/{athlete['id']}")
    assert athlete_detail_response.status_code == 200
    athlete_detail = athlete_detail_response.json()
    assert athlete_detail["full_name"] == athlete_payload["full_name"]
    assert any(item["id"] == roster["id"] for item in athlete_detail.get("rosters", []))

    roster_detail_response = await client.get(f"/api/v1/rosters/{roster['id']}")
    assert roster_detail_response.status_code == 200
    roster_detail = roster_detail_response.json()
    assert roster_detail["owner"]["full_name"] == athlete_payload["full_name"]
    assert roster_detail["club"]["name"] == roster_payload["club"]["name"]
    assert roster_detail["federation"] is None
    assert any(item["id"] == athlete["id"] for item in roster_detail.get("athletes", []))

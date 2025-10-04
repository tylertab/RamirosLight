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

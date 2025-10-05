import pytest

pytestmark = pytest.mark.anyio("asyncio")


async def test_search_returns_federations_clubs_events_and_results(client):
    federation_response = await client.get(
        "/api/v1/search/",
        params={"query": "Federación", "categories": ["federations"]},
    )
    assert federation_response.status_code == 200
    assert any(result["category"] == "Federations" for result in federation_response.json()["results"])

    clubs_response = await client.get(
        "/api/v1/search/",
        params={"query": "Peaks", "categories": ["clubs"]},
    )
    assert clubs_response.status_code == 200
    assert any(result["category"] == "Clubs" for result in clubs_response.json()["results"])

    events_response = await client.get(
        "/api/v1/search/",
        params={"query": "Aurora", "categories": ["events"]},
    )
    assert events_response.status_code == 200
    assert any(result["category"] == "Events" for result in events_response.json()["results"])

    results_response = await client.get(
        "/api/v1/search/",
        params={"query": "Relays", "categories": ["results"]},
    )
    assert results_response.status_code == 200
    assert any(result["category"] == "Results" for result in results_response.json()["results"])


async def test_roster_detail_includes_club_and_federation_context(client):
    rosters_response = await client.get("/api/v1/rosters/")
    assert rosters_response.status_code == 200
    rosters = rosters_response.json()
    assert rosters
    roster = rosters[0]

    detail_response = await client.get(f"/api/v1/rosters/{roster['id']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["club_id"] == roster["club_id"]
    assert detail["club_name"]
    assert detail["federation_id"] is not None
    assert detail["federation_name"]

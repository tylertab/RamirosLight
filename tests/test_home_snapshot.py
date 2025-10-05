import pytest

pytestmark = pytest.mark.anyio("asyncio")


async def test_bootstrap_home_endpoint_returns_data(client):
    response = await client.get("/api/v1/bootstrap/home")
    assert response.status_code == 200
    data = response.json()

    assert "federations" in data and data["federations"]
    first_federation = data["federations"][0]
    assert "clubs" in first_federation
    assert isinstance(first_federation["clubs"], list)
    first_club = first_federation["clubs"][0]
    assert "rosters" in first_club
    assert isinstance(first_club["rosters"], list)

    assert "recent_results" in data and data["recent_results"]
    first_result = data["recent_results"][0]
    assert first_result["event_name"]
    assert first_result["athlete_name"]

    assert "events" in data and data["events"]
    assert data["live_event"]


async def test_templates_embed_initial_data(client):
    home_response = await client.get("/")
    assert home_response.status_code == 200
    assert 'id="initial-home-data"' in home_response.text

    assert '"federations"' in home_response.text
    assert '"recent_results"' in home_response.text

    event_response = await client.get("/events/9999")
    assert event_response.status_code == 200
    assert 'id="initial-event-data"' in event_response.text

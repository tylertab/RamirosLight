import pytest
from uuid import uuid4

pytestmark = pytest.mark.anyio("asyncio")


async def test_event_detail_generation_flow(client):
    unique = uuid4().hex[:6]
    event_payload = {
        "name": f"Continental Cup {unique}",
        "location": "Atlanta, USA",
        "start_date": "2025-03-01",
        "end_date": "2025-03-03",
        "federation_id": None,
    }

    create_response = await client.post("/api/v1/events/", json=event_payload)
    assert create_response.status_code == 201
    event = create_response.json()
    event_id = event["id"]

    demo_response = await client.post(
        f"/api/v1/events/{event_id}/demo",
        json={
            "start_time": "2025-03-01T14:00:00Z",
            "sessions": 2,
            "disciplines_per_session": 2,
            "lanes": 4,
            "include_results": True,
        },
    )
    assert demo_response.status_code == 200
    detail = demo_response.json()
    assert len(detail["sessions"]) == 2
    assert detail["disciplines"]

    first_entry = detail["disciplines"][0]["entries"][0]
    update_response = await client.patch(
        f"/api/v1/events/entries/{first_entry['id']}",
        json={
            "result": "10.05s",
            "status": "finished",
            "points": 14,
            "position": 1,
        },
    )
    assert update_response.status_code == 200
    updated_entry = update_response.json()
    assert updated_entry["result"] == "10.05s"
    assert updated_entry["status"] == "finished"

    session_response = await client.post(
        f"/api/v1/events/{event_id}/sessions",
        json={
            "name": "Relay Finals",
            "status": "scheduled",
        },
    )
    assert session_response.status_code == 201
    session_id = session_response.json()["id"]

    discipline_response = await client.post(
        f"/api/v1/events/{event_id}/disciplines",
        json={
            "name": "4x400m Relay",
            "session_id": session_id,
            "status": "scheduled",
        },
    )
    assert discipline_response.status_code == 201
    discipline_id = discipline_response.json()["id"]

    entry_response = await client.post(
        f"/api/v1/events/disciplines/{discipline_id}/entries",
        json={
            "athlete_name": "Demo Team",
            "team_name": "Demo Team",
            "status": "scheduled",
        },
    )
    assert entry_response.status_code == 201

    final_detail_response = await client.get(f"/api/v1/events/{event_id}")
    assert final_detail_response.status_code == 200
    final_detail = final_detail_response.json()
    assert any(session["id"] == session_id for session in final_detail["sessions"])
    assert any(discipline["id"] == discipline_id for discipline in final_detail["disciplines"])
    assert final_detail["latest_update"] is not None

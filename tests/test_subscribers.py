import pytest

pytestmark = pytest.mark.anyio("asyncio")


async def test_subscriber_endpoint_accepts_new_email(client):
    payload = {"email": "subscriber@example.com", "locale": "en"}
    response = await client.post("/api/v1/subscribers/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == payload["email"]
    assert body["locale"] == payload["locale"]


async def test_subscriber_endpoint_is_idempotent(client):
    payload = {"email": "duplicate@example.com", "locale": "es"}
    first = await client.post("/api/v1/subscribers/", json=payload)
    assert first.status_code == 201
    duplicate = await client.post("/api/v1/subscribers/", json=payload)
    assert duplicate.status_code == 201
    assert duplicate.json()["id"] == first.json()["id"]

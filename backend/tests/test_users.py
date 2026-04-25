import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _admin_token(client: AsyncClient) -> str:
    res = await client.post("/auth/login", json={
        "email": "admin@example.com", "password": "adminpass123"
    })
    return res.json()["access_token"]


async def _employee_token(client: AsyncClient) -> str:
    res = await client.post("/auth/login", json={
        "email": "employee@example.com", "password": "emppass123"
    })
    return res.json()["access_token"]


async def test_list_users_employee_forbidden(client: AsyncClient, employee_user):
    token = await _employee_token(client)
    res = await client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403


async def test_list_users_returns_all(client: AsyncClient, admin_user, employee_user):
    token = await _admin_token(client)
    res = await client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 2
    emails = [u["email"] for u in data["users"]]
    assert "admin@example.com" in emails
    assert "employee@example.com" in emails


async def test_delete_user_not_found(client: AsyncClient, admin_user):
    token = await _admin_token(client)
    res = await client.delete("/users/99999", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_employee(client: AsyncClient):
    res = await client.post("/auth/register", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret123",
        "role": "employee",
    })
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_register_duplicate_email(client: AsyncClient):
    payload = {"name": "Jane", "email": "jane@example.com", "password": "pass", "role": "employee"}
    await client.post("/auth/register", json=payload)
    res = await client.post("/auth/register", json=payload)
    assert res.status_code == 409
    assert res.json()["detail"] == "Email already registered"


async def test_login_success(client: AsyncClient, employee_user):
    res = await client.post("/auth/login", json={
        "email": "employee@example.com",
        "password": "emppass123",
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


async def test_login_wrong_password(client: AsyncClient, employee_user):
    res = await client.post("/auth/login", json={
        "email": "employee@example.com",
        "password": "wrongpassword",
    })
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"


async def test_me_returns_user(client: AsyncClient, admin_user):
    login_res = await client.post("/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpass123",
    })
    token = login_res.json()["access_token"]
    res = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "admin@example.com"
    assert data["role"] == "admin"


async def test_me_no_token(client: AsyncClient):
    res = await client.get("/auth/me")
    assert res.status_code == 403

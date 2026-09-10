import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "strongpassword123",
        "phone_number": "09123456789"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "full_name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "strongpassword123",
        "phone_number": "09123456780"
    }
    
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    payload = {
        "full_name": "Login User",
        "email": "login@example.com",
        "password": "password123",
    }
    await client.post("/auth/register", json=payload)
    
    login_data = {
        "username": "login@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    login_data = {
        "username": "wrong@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."
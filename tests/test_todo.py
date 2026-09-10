import pytest
from httpx import AsyncClient
import pytest_asyncio

@pytest_asyncio.fixture
async def setup_users(client: AsyncClient):
    """Creates two isolated users and returns their auth headers."""
    users_data = []
    for i in range(1, 3):
        user = {
            "full_name": f"User {i}",
            "email": f"user{i}@example.com",
            "password": "password123"
        }
        await client.post("/auth/register", json=user)
        res = await client.post("/auth/login", data={"username": user["email"], "password": user["password"]})
        token = res.json()["access_token"]
        users_data.append({"headers": {"Authorization": f"Bearer {token}"}})
    
    return {"user1": users_data[0], "user2": users_data[1]}


@pytest.mark.asyncio
async def test_create_todo_success(client: AsyncClient, setup_users):
    headers = setup_users["user1"]["headers"]
    payload = {
        "title": "Buy milk",
        "description": "2 liters of milk",
        "priority": 1
    }
    
    response = await client.post("/todos/", json=payload, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_bola_protection_prevent_access_to_others_todo(client: AsyncClient, setup_users):
    # User 1 creates a highly private Todo
    headers_user1 = setup_users["user1"]["headers"]
    todo_payload = {"title": "User 1 Private Task"}
    create_res = await client.post("/todos/", json=todo_payload, headers=headers_user1)
    todo_id = create_res.json()["id"]

    # User 2 attempts to fetch User 1's Todo
    headers_user2 = setup_users["user2"]["headers"]
    fetch_res = await client.get(f"/todos/{todo_id}", headers=headers_user2)
    
    # Assert BOLA protection correctly returns 404 (Not Found) to prevent data leakage
    assert fetch_res.status_code == 404


@pytest.mark.asyncio
async def test_update_todo_success(client: AsyncClient, setup_users):
    headers = setup_users["user1"]["headers"]
    create_res = await client.post("/todos/", json={"title": "Old Title"}, headers=headers)
    todo_id = create_res.json()["id"]
    
    update_payload = {"title": "New Title", "status": "completed"}
    response = await client.put(f"/todos/{todo_id}", json=update_payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_todo_success(client: AsyncClient, setup_users):
    headers = setup_users["user1"]["headers"]
    create_res = await client.post("/todos/", json={"title": "To be deleted"}, headers=headers)
    todo_id = create_res.json()["id"]
    
    delete_res = await client.delete(f"/todos/{todo_id}", headers=headers)
    assert delete_res.status_code == 204
    
    # Verify deletion
    fetch_res = await client.get(f"/todos/{todo_id}", headers=headers)
    assert fetch_res.status_code == 404
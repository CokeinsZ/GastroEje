import pytest
from httpx import AsyncClient
from app.models.users import UserRole, UserStatus

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user_id"] is not None

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # First register
    await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    
    # Then login
    response = await client.post("/usuarios/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_get_user_list(client: AsyncClient):
    # Register a user to get token
    reg_response = await client.post("/usuarios/register", json={
        "name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "admin",
        "status": "active"
    })
    token = reg_response.json()["access_token"]
    
    response = await client.get("/usuarios/list", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    response = await client.get(f"/usuarios/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "test@example.com"
    assert user_data["user_id"] == user_id

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    response = await client.put(f"/usuarios/{user_id}", json={
        "name": "Updated Name",
        "last_name": "Updated Last Name",
        "phone": "0987654321"
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Updated Name"
    assert updated_user["last_name"] == "Updated Last Name"
    assert updated_user["phone"] == "0987654321"

@pytest.mark.asyncio
async def test_change_password(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    response = await client.patch(f"/usuarios/{user_id}/password", json={
        "current_password": "password123",
        "new_password": "newpassword456"
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    
    # Verify login with new password
    login_response = await client.post("/usuarios/login", json={
        "email": "test@example.com",
        "password": "newpassword456"
    })
    assert login_response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    response = await client.delete(f"/usuarios/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    
    # Verify user is gone (or handled as deleted)
    # Depending on implementation, it might return 404 or 200 with empty body, etc.
    # Assuming 404 for get by id
    get_response = await client.get(f"/usuarios/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_get_user_by_email(client: AsyncClient):
    # Register a user
    email = "emailtest@example.com"
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": email,
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    token = reg_response.json()["access_token"]
    
    response = await client.get(f"/usuarios/email/{email}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email

@pytest.mark.asyncio
async def test_change_role(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "roletest@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    response = await client.patch(f"/usuarios/{user_id}/role", json={
        "role": "admin"
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    
    # Verify role change
    get_response = await client.get(f"/usuarios/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.json()["role"] == "admin"

@pytest.mark.asyncio
async def test_change_status(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "statustest@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    response = await client.patch(f"/usuarios/{user_id}/status", json={
        "status": "inactive"
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    
    # Verify status change
    get_response = await client.get(f"/usuarios/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.json()["status"] == "inactive"

@pytest.mark.asyncio
async def test_update_allergens(client: AsyncClient):
    # Register a user
    reg_response = await client.post("/usuarios/register", json={
        "name": "Test",
        "last_name": "User",
        "email": "allergentest@example.com",
        "password": "password123",
        "phone": "1234567890",
        "role": "user",
        "status": "active"
    })
    data = reg_response.json()
    user_id = data["user_id"]
    token = data["access_token"]
    
    # Currently the endpoint doesn't take a body, just returns success
    response = await client.patch(f"/usuarios/{user_id}/allergens", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Allergens updated successfully"

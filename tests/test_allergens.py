import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_allergen(client: AsyncClient):
    """Test crear un nuevo alérgeno"""
    payload = {
        "name": "Gluten"
    }
    
    response = await client.post("/allergen/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gluten"
    assert "allergen_id" in data


@pytest.mark.asyncio
async def test_list_allergens(client: AsyncClient):
    """Test listar todos los alérgenos"""
    # Create allergens first
    allergens = ["Lactosa", "Soya", "Maní"]
    for allergen in allergens:
        await client.post("/allergen/", json={"name": allergen})
    
    response = await client.get("/allergen/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_get_allergen_by_id(client: AsyncClient):
    """Test obtener un alérgeno por ID"""
    # Create allergen
    create_response = await client.post("/allergen/", json={"name": "Huevo"})
    created_data = create_response.json()
    allergen_id = created_data["allergen_id"]
    
    # Get allergen
    response = await client.get(f"/allergen/{allergen_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["allergen_id"] == allergen_id
    assert data["name"] == "Huevo"


@pytest.mark.asyncio
async def test_get_allergen_not_found(client: AsyncClient):
    """Test obtener un alérgeno inexistente retorna 404"""
    response = await client.get("/allergen/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_allergen(client: AsyncClient):
    """Test actualizar un alérgeno"""
    # Create allergen
    create_response = await client.post("/allergen/", json={"name": "Nuez"})
    created_data = create_response.json()
    allergen_id = created_data["allergen_id"]
    
    # Update allergen
    update_payload = {"name": "Nueces"}
    response = await client.put(f"/allergen/{allergen_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Nueces"
    
    # Verify update
    get_response = await client.get(f"/allergen/{allergen_id}")
    assert get_response.json()["name"] == "Nueces"


@pytest.mark.asyncio
async def test_delete_allergen(client: AsyncClient):
    """Test eliminar un alérgeno"""
    # Create allergen
    create_response = await client.post("/allergen/", json={"name": "Pescado"})
    created_data = create_response.json()
    allergen_id = created_data["allergen_id"]
    
    # Delete allergen
    response = await client.delete(f"/allergen/{allergen_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify deletion
    get_response = await client.get(f"/allergen/{allergen_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_add_allergen_to_user(client: AsyncClient):
    """Test asociar un alérgeno a un usuario"""
    # Create user
    user_payload = {
        "name": "John",
        "last_name": "Doe",
        "email": "john.allergen@test.com",
        "password": "Password123!",
        "role": "user",
        "status": "active"
    }
    user_response = await client.post("/usuarios/register", json=user_payload)
    user_data = user_response.json()
    user_id = user_data["user_id"]
    
    # Create allergen
    allergen_response = await client.post("/allergen/", json={"name": "Mariscos"})
    allergen_data = allergen_response.json()
    allergen_id = allergen_data["allergen_id"]
    
    # Associate allergen to user
    response = await client.post(f"/allergen/user/{user_id}/allergen/{allergen_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify association
    user_allergens = await client.get(f"/allergen/user/{user_id}")
    assert user_allergens.status_code == 200
    allergens = user_allergens.json()
    assert len(allergens) >= 1
    assert any(a["allergen_id"] == allergen_id for a in allergens)


@pytest.mark.asyncio
async def test_remove_allergen_from_user(client: AsyncClient):
    """Test desasociar un alérgeno de un usuario"""
    # Create user
    user_payload = {
        "name": "Jane",
        "last_name": "Smith",
        "email": "jane.allergen@test.com",
        "password": "Password123!",
        "role": "user",
        "status": "active"
    }
    user_response = await client.post("/usuarios/register", json=user_payload)
    user_data = user_response.json()
    user_id = user_data["user_id"]
    
    # Create allergen
    allergen_response = await client.post("/allergen/", json={"name": "Trigo"})
    allergen_data = allergen_response.json()
    allergen_id = allergen_data["allergen_id"]
    
    # Associate allergen to user
    await client.post(f"/allergen/user/{user_id}/allergen/{allergen_id}")
    
    # Remove association
    response = await client.delete(f"/allergen/user/{user_id}/allergen/{allergen_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify removal
    user_allergens = await client.get(f"/allergen/user/{user_id}")
    allergens = user_allergens.json()
    assert not any(a["allergen_id"] == allergen_id for a in allergens)


@pytest.mark.asyncio
async def test_get_allergens_by_user(client: AsyncClient):
    """Test obtener todos los alérgenos de un usuario"""
    # Create user
    user_payload = {
        "name": "Alice",
        "last_name": "Wonder",
        "email": "alice.allergen@test.com",
        "password": "Password123!",
        "role": "user",
        "status": "active"
    }
    user_response = await client.post("/usuarios/register", json=user_payload)
    user_data = user_response.json()
    user_id = user_data["user_id"]
    
    # Create multiple allergens
    allergens_to_create = ["Almendras", "Avellanas", "Cacahuates"]
    allergen_ids = []
    for allergen_name in allergens_to_create:
        allergen_response = await client.post("/allergen/", json={"name": allergen_name})
        allergen_ids.append(allergen_response.json()["allergen_id"])
    
    # Associate allergens to user
    for allergen_id in allergen_ids:
        await client.post(f"/allergen/user/{user_id}/allergen/{allergen_id}")
    
    # Get user allergens
    response = await client.get(f"/allergen/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    allergen_names = [a["name"] for a in data]
    for name in allergens_to_create:
        assert name in allergen_names


@pytest.mark.asyncio
async def test_get_allergens_by_user_empty(client: AsyncClient):
    """Test obtener alérgenos de un usuario sin alérgenos"""
    # Create user
    user_payload = {
        "name": "Bob",
        "last_name": "Builder",
        "email": "bob.noallergen@test.com",
        "password": "Password123!",
        "role": "user",
        "status": "active"
    }
    user_response = await client.post("/usuarios/register", json=user_payload)
    user_data = user_response.json()
    user_id = user_data["user_id"]
    
    # Get user allergens (should be empty)
    response = await client.get(f"/allergen/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

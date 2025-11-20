import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_establishment(client: AsyncClient):
    # Prepare data
    opening_hour = datetime.now().time().isoformat()
    closing_hour = (datetime.now() + timedelta(hours=8)).time().isoformat()
    
    payload = {
        "NIT": "123456789",
        "name": "Test Restaurant",
        "description": "A nice place",
        "sustainability_points": 10,
        "address": "123 Test St",
        "mean_waiting_time": 15.5,
        "opening_hour": opening_hour,
        "closing_hour": closing_hour,
        "phone_number": "1234567890",
        "website": "http://test.com",
        "logo": "http://test.com/logo.png"
    }
    
    response = await client.post("/establishments/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Restaurant"
    assert data["NIT"] == "123456789"
    assert "establishment_id" in data

@pytest.mark.asyncio
async def test_list_establishments(client: AsyncClient):
    # Create an establishment first
    opening_hour = datetime.now().time().isoformat()
    closing_hour = (datetime.now() + timedelta(hours=8)).time().isoformat()
    
    payload = {
        "NIT": "987654321",
        "name": "List Test Restaurant",
        "address": "456 List St",
        "opening_hour": opening_hour,
        "closing_hour": closing_hour
    }
    await client.post("/establishments/", json=payload)
    
    response = await client.get("/establishments/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

@pytest.mark.asyncio
async def test_get_establishment_by_id(client: AsyncClient):
    # Create an establishment
    opening_hour = datetime.now().time().isoformat()
    closing_hour = (datetime.now() + timedelta(hours=8)).time().isoformat()
    
    payload = {
        "NIT": "1122334455",
        "name": "Get One Restaurant",
        "address": "789 Get St",
        "opening_hour": opening_hour,
        "closing_hour": closing_hour
    }
    create_response = await client.post("/establishments/", json=payload)
    created_data = create_response.json()
    est_id = created_data["establishment_id"]
    
    response = await client.get(f"/establishments/{est_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["establishment_id"] == est_id
    assert data["name"] == "Get One Restaurant"

@pytest.mark.asyncio
async def test_update_establishment(client: AsyncClient):
    # Create an establishment
    opening_hour = datetime.now().time().isoformat()
    closing_hour = (datetime.now() + timedelta(hours=8)).time().isoformat()
    
    payload = {
        "NIT": "5544332211",
        "name": "Update Restaurant",
        "address": "321 Update St",
        "opening_hour": opening_hour,
        "closing_hour": closing_hour
    }
    create_response = await client.post("/establishments/", json=payload)
    created_data = create_response.json()
    est_id = created_data["establishment_id"]
    
    # Update
    update_payload = {
        "name": "Updated Restaurant Name",
        "description": "Updated description"
    }
    response = await client.patch(f"/establishments/{est_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Restaurant Name"
    assert data["description"] == "Updated description"
    
    # Verify with get
    get_response = await client.get(f"/establishments/{est_id}")
    assert get_response.json()["name"] == "Updated Restaurant Name"

@pytest.mark.asyncio
async def test_delete_establishment(client: AsyncClient):
    # Create an establishment
    opening_hour = datetime.now().time().isoformat()
    closing_hour = (datetime.now() + timedelta(hours=8)).time().isoformat()
    
    payload = {
        "NIT": "9988776655",
        "name": "Delete Restaurant",
        "address": "654 Delete St",
        "opening_hour": opening_hour,
        "closing_hour": closing_hour
    }
    create_response = await client.post("/establishments/", json=payload)
    created_data = create_response.json()
    est_id = created_data["establishment_id"]
    
    # Delete
    response = await client.delete(f"/establishments/{est_id}")
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify it's gone
    get_response = await client.get(f"/establishments/{est_id}")
    assert get_response.status_code == 404

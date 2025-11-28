import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


async def create_test_user(client: AsyncClient, email: str, name: str, phone: str):
    """Helper para crear usuarios de prueba"""
    user_payload = {
        "email": email,
        "password": "password123",
        "name": name,
        "phone": phone,
        "role": "user",
        "status": "active"
    }
    response = await client.post("/usuarios/register", json=user_payload)
    return response.json()["user_id"]


@pytest.mark.asyncio
async def test_create_reservation(client: AsyncClient):
    """Test crear una nueva reserva"""
    # Crear usuario
    user_id = await create_test_user(client, "reservation_user@test.com", "Reservation User", "1234567890")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123456789",
        "name": "Reservation Restaurant",
        "address": "123 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reserva
    reservation_date = (datetime.now() + timedelta(days=1)).isoformat()
    reservation_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "date": reservation_date,
        "people_count": 4
    }
    response = await client.post("/reservas/", json=reservation_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["establishment_id"] == establishment_id
    assert data["people_count"] == 4
    assert data["status"] == "pending"
    assert "reservation_id" in data


@pytest.mark.asyncio
async def test_create_reservation_user_not_found(client: AsyncClient):
    """Test crear reserva con usuario inexistente debe fallar"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "987654321",
        "name": "No User Restaurant",
        "address": "456 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Intentar crear reserva con usuario inexistente
    reservation_date = (datetime.now() + timedelta(days=1)).isoformat()
    reservation_payload = {
        "user_id": 99999,
        "establishment_id": establishment_id,
        "date": reservation_date,
        "people_count": 2
    }
    response = await client.post("/reservas/", json=reservation_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_reservation_establishment_not_found(client: AsyncClient):
    """Test crear reserva con establecimiento inexistente debe fallar"""
    # Crear usuario
    user_id = await create_test_user(client, "noest_user@test.com", "No Est User", "9876543210")
    
    # Intentar crear reserva con establecimiento inexistente
    reservation_date = (datetime.now() + timedelta(days=1)).isoformat()
    reservation_payload = {
        "user_id": user_id,
        "establishment_id": 99999,
        "date": reservation_date,
        "people_count": 2
    }
    response = await client.post("/reservas/", json=reservation_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_reservations(client: AsyncClient):
    """Test listar todas las reservas"""
    # Crear usuario
    user_id = await create_test_user(client, "list_user@test.com", "List User", "1112223333")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "111222333",
        "name": "List Restaurant",
        "address": "789 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear varias reservas
    people_counts = [2, 4, 6]
    for count in people_counts:
        reservation_date = (datetime.now() + timedelta(days=count)).isoformat()
        reservation_payload = {
            "user_id": user_id,
            "establishment_id": establishment_id,
            "date": reservation_date,
            "people_count": count
        }
        await client.post("/reservas/", json=reservation_payload)
    
    # Listar reservas
    response = await client.get("/reservas/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_get_reservation(client: AsyncClient):
    """Test obtener una reserva específica"""
    # Crear usuario
    user_id = await create_test_user(client, "get_user@test.com", "Get User", "4445556666")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "444555666",
        "name": "Get Restaurant",
        "address": "321 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reserva
    reservation_date = (datetime.now() + timedelta(days=2)).isoformat()
    reservation_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "date": reservation_date,
        "people_count": 3
    }
    create_response = await client.post("/reservas/", json=reservation_payload)
    reservation_id = create_response.json()["reservation_id"]
    
    # Obtener reserva
    response = await client.get(f"/reservas/{reservation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["reservation_id"] == reservation_id
    assert data["people_count"] == 3


@pytest.mark.asyncio
async def test_get_reservation_not_found(client: AsyncClient):
    """Test obtener reserva inexistente debe fallar"""
    response = await client.get("/reservas/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_reservation(client: AsyncClient):
    """Test actualizar una reserva"""
    # Crear usuario
    user_id = await create_test_user(client, "update_user@test.com", "Update User", "7778889999")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "777888999",
        "name": "Update Restaurant",
        "address": "654 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reserva
    reservation_date = (datetime.now() + timedelta(days=3)).isoformat()
    reservation_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "date": reservation_date,
        "people_count": 2
    }
    create_response = await client.post("/reservas/", json=reservation_payload)
    reservation_id = create_response.json()["reservation_id"]
    
    # Actualizar reserva
    new_date = (datetime.now() + timedelta(days=5)).isoformat()
    update_payload = {
        "date": new_date,
        "people_count": 6
    }
    response = await client.put(f"/reservas/{reservation_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["people_count"] == 6


@pytest.mark.asyncio
async def test_update_reservation_not_found(client: AsyncClient):
    """Test actualizar reserva inexistente debe fallar"""
    update_payload = {
        "people_count": 5
    }
    response = await client.put("/reservas/99999", json=update_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cancel_reservation(client: AsyncClient):
    """Test cancelar una reserva"""
    # Crear usuario
    user_id = await create_test_user(client, "cancel_user@test.com", "Cancel User", "1231231234")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123123123",
        "name": "Cancel Restaurant",
        "address": "111 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reserva
    reservation_date = (datetime.now() + timedelta(days=4)).isoformat()
    reservation_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "date": reservation_date,
        "people_count": 3
    }
    create_response = await client.post("/reservas/", json=reservation_payload)
    reservation_id = create_response.json()["reservation_id"]
    
    # Cancelar reserva
    response = await client.patch(f"/reservas/{reservation_id}/cancelar")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"
    
    # Verificar que el estado cambió
    get_response = await client.get(f"/reservas/{reservation_id}")
    assert get_response.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_reservation_not_found(client: AsyncClient):
    """Test cancelar reserva inexistente debe fallar"""
    response = await client.patch("/reservas/99999/cancelar")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_reservation(client: AsyncClient):
    """Test eliminar una reserva"""
    # Crear usuario
    user_id = await create_test_user(client, "delete_user@test.com", "Delete User", "4564564567")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "456456456",
        "name": "Delete Restaurant",
        "address": "222 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reserva
    reservation_date = (datetime.now() + timedelta(days=6)).isoformat()
    reservation_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "date": reservation_date,
        "people_count": 5
    }
    create_response = await client.post("/reservas/", json=reservation_payload)
    reservation_id = create_response.json()["reservation_id"]
    
    # Eliminar reserva
    response = await client.delete(f"/reservas/{reservation_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verificar que fue eliminada
    get_response = await client.get(f"/reservas/{reservation_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_reservation_not_found(client: AsyncClient):
    """Test eliminar reserva inexistente debe fallar"""
    response = await client.delete("/reservas/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_reservations_by_user(client: AsyncClient):
    """Test obtener todas las reservas de un usuario"""
    # Crear usuario
    user_id = await create_test_user(client, "user_reservations@test.com", "User Reservations", "7897897890")
    
    # Crear establecimientos
    establishments = []
    for i in range(2):
        est_payload = {
            "NIT": f"789789{i}",
            "name": f"Restaurant {i}",
            "address": f"{i} Test St",
            "opening_hour": "08:00:00",
            "closing_hour": "22:00:00"
        }
        est_response = await client.post("/establishments/", json=est_payload)
        establishments.append(est_response.json()["establishment_id"])
    
    # Crear múltiples reservas para el usuario
    for i, est_id in enumerate(establishments):
        reservation_date = (datetime.now() + timedelta(days=i+1)).isoformat()
        reservation_payload = {
            "user_id": user_id,
            "establishment_id": est_id,
            "date": reservation_date,
            "people_count": i + 2
        }
        await client.post("/reservas/", json=reservation_payload)
    
    # Obtener reservas del usuario
    response = await client.get(f"/reservas/usuario/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for reservation in data:
        assert reservation["user_id"] == user_id


@pytest.mark.asyncio
async def test_get_reservations_by_establishment(client: AsyncClient):
    """Test obtener todas las reservas de un establecimiento"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "321321321",
        "name": "Est Reservations Restaurant",
        "address": "333 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear múltiples usuarios
    user_ids = []
    for i in range(3):
        user_id = await create_test_user(client, f"est_user{i}@test.com", f"Est User {i}", f"32132132{i}")
        user_ids.append(user_id)
    
    # Crear reservas de diferentes usuarios para el mismo establecimiento
    for i, user_id in enumerate(user_ids):
        reservation_date = (datetime.now() + timedelta(days=i+1)).isoformat()
        reservation_payload = {
            "user_id": user_id,
            "establishment_id": establishment_id,
            "date": reservation_date,
            "people_count": i + 2
        }
        await client.post("/reservas/", json=reservation_payload)
    
    # Obtener reservas del establecimiento
    response = await client.get(f"/reservas/establecimiento/{establishment_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for reservation in data:
        assert reservation["establishment_id"] == establishment_id


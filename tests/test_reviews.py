import pytest
from httpx import AsyncClient


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
async def test_create_review(client: AsyncClient):
    """Test crear una nueva reseña"""
    # Crear usuario
    user_id = await create_test_user(client, "review_user@test.com", "Review User", "1234567890")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123456789",
        "name": "Review Restaurant",
        "address": "123 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reseña
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "5",
        "comment": "Excelente restaurante"
    }
    response = await client.post("/resenas/", json=review_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["establishment_id"] == establishment_id
    assert data["rating"] == "5"
    assert data["comment"] == "Excelente restaurante"


@pytest.mark.asyncio
async def test_create_review_user_not_found(client: AsyncClient):
    """Test crear reseña con usuario inexistente debe fallar"""
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
    
    # Intentar crear reseña con usuario inexistente
    review_payload = {
        "user_id": 99999,
        "establishment_id": establishment_id,
        "rating": "4"
    }
    response = await client.post("/resenas/", json=review_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_review_establishment_not_found(client: AsyncClient):
    """Test crear reseña con establecimiento inexistente debe fallar"""
    # Crear usuario
    user_id = await create_test_user(client, "noest_review@test.com", "No Est Review", "9876543210")
    
    # Intentar crear reseña con establecimiento inexistente
    review_payload = {
        "user_id": user_id,
        "establishment_id": 99999,
        "rating": "3"
    }
    response = await client.post("/resenas/", json=review_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate_review(client: AsyncClient):
    """Test crear reseña duplicada (mismo usuario y establecimiento) debe fallar"""
    # Crear usuario
    user_id = await create_test_user(client, "duplicate_review@test.com", "Duplicate Review", "1112223333")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "111222333",
        "name": "Duplicate Restaurant",
        "address": "789 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear primera reseña
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "4",
        "comment": "Primera reseña"
    }
    await client.post("/resenas/", json=review_payload)
    
    # Intentar crear segunda reseña del mismo usuario para el mismo establecimiento
    response = await client.post("/resenas/", json=review_payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_reviews(client: AsyncClient):
    """Test listar todas las reseñas"""
    # Crear usuario
    user_id = await create_test_user(client, "list_review@test.com", "List Review", "4445556666")
    
    # Crear establecimientos
    establishments = []
    for i in range(3):
        est_payload = {
            "NIT": f"444555{i}",
            "name": f"List Restaurant {i}",
            "address": f"{i} Test St",
            "opening_hour": "08:00:00",
            "closing_hour": "22:00:00"
        }
        est_response = await client.post("/establishments/", json=est_payload)
        establishments.append(est_response.json()["establishment_id"])
    
    # Crear reseñas
    for est_id in establishments:
        review_payload = {
            "user_id": user_id,
            "establishment_id": est_id,
            "rating": "5"
        }
        await client.post("/resenas/", json=review_payload)
    
    # Listar reseñas
    response = await client.get("/resenas/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_get_review(client: AsyncClient):
    """Test obtener una reseña específica"""
    # Crear usuario
    user_id = await create_test_user(client, "get_review@test.com", "Get Review", "7778889999")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "777888999",
        "name": "Get Review Restaurant",
        "address": "321 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reseña
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "4",
        "comment": "Muy bueno"
    }
    await client.post("/resenas/", json=review_payload)
    
    # Obtener reseña
    response = await client.get(f"/resenas/usuario/{user_id}/establecimiento/{establishment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["establishment_id"] == establishment_id
    assert data["rating"] == "4"


@pytest.mark.asyncio
async def test_get_review_not_found(client: AsyncClient):
    """Test obtener reseña inexistente debe fallar"""
    response = await client.get("/resenas/usuario/99999/establecimiento/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_by_establishment(client: AsyncClient):
    """Test obtener todas las reseñas de un establecimiento"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123123123",
        "name": "Est Reviews Restaurant",
        "address": "654 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear múltiples usuarios y reseñas
    ratings = ["5", "4", "3"]
    for i, rating in enumerate(ratings):
        user_id = await create_test_user(
            client,
            f"est_review_{i}@test.com",
            f"Est Review {i}",
            f"12312312{i}"
        )
        review_payload = {
            "user_id": user_id,
            "establishment_id": establishment_id,
            "rating": rating,
            "comment": f"Comentario {i}"
        }
        await client.post("/resenas/", json=review_payload)
    
    # Obtener reseñas del establecimiento
    response = await client.get(f"/resenas/establecimiento/{establishment_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for review in data:
        assert review["establishment_id"] == establishment_id


@pytest.mark.asyncio
async def test_get_reviews_by_user(client: AsyncClient):
    """Test obtener todas las reseñas de un usuario"""
    # Crear usuario
    user_id = await create_test_user(client, "user_reviews@test.com", "User Reviews", "4564564567")
    
    # Crear múltiples establecimientos
    establishments = []
    for i in range(2):
        est_payload = {
            "NIT": f"456456{i}",
            "name": f"User Review Restaurant {i}",
            "address": f"{i} Test St",
            "opening_hour": "08:00:00",
            "closing_hour": "22:00:00"
        }
        est_response = await client.post("/establishments/", json=est_payload)
        establishments.append(est_response.json()["establishment_id"])
    
    # Crear reseñas del usuario para diferentes establecimientos
    for est_id in establishments:
        review_payload = {
            "user_id": user_id,
            "establishment_id": est_id,
            "rating": "5"
        }
        await client.post("/resenas/", json=review_payload)
    
    # Obtener reseñas del usuario
    response = await client.get(f"/resenas/usuario/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for review in data:
        assert review["user_id"] == user_id


@pytest.mark.asyncio
async def test_update_review(client: AsyncClient):
    """Test actualizar una reseña"""
    # Crear usuario
    user_id = await create_test_user(client, "update_review@test.com", "Update Review", "7897897890")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "789789789",
        "name": "Update Review Restaurant",
        "address": "111 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reseña
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "3",
        "comment": "Regular"
    }
    await client.post("/resenas/", json=review_payload)
    
    # Actualizar reseña
    update_payload = {
        "rating": "5",
        "comment": "Ahora es excelente"
    }
    response = await client.put(
        f"/resenas/usuario/{user_id}/establecimiento/{establishment_id}",
        json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == "5"
    assert data["comment"] == "Ahora es excelente"


@pytest.mark.asyncio
async def test_update_review_partial(client: AsyncClient):
    """Test actualización parcial de reseña"""
    # Crear usuario
    user_id = await create_test_user(client, "partial_review@test.com", "Partial Review", "3213213210")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "321321321",
        "name": "Partial Review Restaurant",
        "address": "222 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reseña
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "4",
        "comment": "Comentario original"
    }
    await client.post("/resenas/", json=review_payload)
    
    # Actualizar solo el comentario
    update_payload = {
        "comment": "Comentario actualizado"
    }
    response = await client.put(
        f"/resenas/usuario/{user_id}/establecimiento/{establishment_id}",
        json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == "4"  # No cambió
    assert data["comment"] == "Comentario actualizado"


@pytest.mark.asyncio
async def test_update_review_not_found(client: AsyncClient):
    """Test actualizar reseña inexistente debe fallar"""
    update_payload = {
        "rating": "5"
    }
    response = await client.put(
        "/resenas/usuario/99999/establecimiento/99999",
        json=update_payload
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_review(client: AsyncClient):
    """Test eliminar una reseña"""
    # Crear usuario
    user_id = await create_test_user(client, "delete_review@test.com", "Delete Review", "6546546540")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "654654654",
        "name": "Delete Review Restaurant",
        "address": "333 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reseña
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "2"
    }
    await client.post("/resenas/", json=review_payload)
    
    # Eliminar reseña
    response = await client.delete(f"/resenas/usuario/{user_id}/establecimiento/{establishment_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verificar que fue eliminada
    get_response = await client.get(f"/resenas/usuario/{user_id}/establecimiento/{establishment_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_review_not_found(client: AsyncClient):
    """Test eliminar reseña inexistente debe fallar"""
    response = await client.delete("/resenas/usuario/99999/establecimiento/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_review_without_comment(client: AsyncClient):
    """Test crear reseña sin comentario (campo opcional)"""
    # Crear usuario
    user_id = await create_test_user(client, "nocomment_review@test.com", "No Comment", "9879879870")
    
    # Crear establecimiento
    establishment_payload = {
        "NIT": "987987987",
        "name": "No Comment Restaurant",
        "address": "444 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear reseña sin comentario
    review_payload = {
        "user_id": user_id,
        "establishment_id": establishment_id,
        "rating": "5"
    }
    response = await client.post("/resenas/", json=review_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == "5"
    assert data["comment"] is None


@pytest.mark.asyncio
async def test_create_review_with_all_ratings(client: AsyncClient):
    """Test crear reseñas con todos los valores de rating posibles"""
    # Crear usuario
    user_id = await create_test_user(client, "ratings_review@test.com", "Ratings Review", "1471471470")
    
    # Probar todos los ratings
    ratings = ["1", "2", "3", "4", "5"]
    for i, rating in enumerate(ratings):
        # Crear establecimiento
        est_payload = {
            "NIT": f"14714714{i}",
            "name": f"Rating {rating} Restaurant",
            "address": f"{i} Test St",
            "opening_hour": "08:00:00",
            "closing_hour": "22:00:00"
        }
        est_response = await client.post("/establishments/", json=est_payload)
        establishment_id = est_response.json()["establishment_id"]
        
        # Crear reseña con este rating
        review_payload = {
            "user_id": user_id,
            "establishment_id": establishment_id,
            "rating": rating
        }
        response = await client.post("/resenas/", json=review_payload)
        assert response.status_code == 201
        assert response.json()["rating"] == rating

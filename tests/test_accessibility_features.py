import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_accessibility_feature(client: AsyncClient):
    """Test crear una característica de accesibilidad"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123456789",
        "name": "Accessible Restaurant",
        "address": "123 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear característica de accesibilidad
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Rampa de acceso",
        "description": "Rampa en la entrada principal"
    }
    response = await client.post("/accessibilidad/", json=feature_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Accessibility feature created successfully"
    assert "feature_id" in data


@pytest.mark.asyncio
async def test_create_accessibility_feature_duplicate(client: AsyncClient):
    """Test crear característica duplicada debe fallar"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "987654321",
        "name": "Duplicate Feature Restaurant",
        "address": "456 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear primera característica
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Baño adaptado",
        "description": "Baño con barras de apoyo"
    }
    await client.post("/accessibilidad/", json=feature_payload)
    
    # Intentar crear característica duplicada (mismo nombre y establecimiento)
    response = await client.post("/accessibilidad/", json=feature_payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_accessibility_feature_same_name_different_establishment(client: AsyncClient):
    """Test crear característica con mismo nombre en diferentes establecimientos"""
    # Crear dos establecimientos
    establishments = []
    for i in range(2):
        est_payload = {
            "NIT": f"111222{i}",
            "name": f"Restaurant {i}",
            "address": f"{i} Test St",
            "opening_hour": "08:00:00",
            "closing_hour": "22:00:00"
        }
        est_response = await client.post("/establishments/", json=est_payload)
        establishments.append(est_response.json()["establishment_id"])
    
    # Crear característica con mismo nombre en ambos establecimientos
    feature_name = "Estacionamiento adaptado"
    for establishment_id in establishments:
        feature_payload = {
            "establishment_id": establishment_id,
            "name": feature_name,
            "description": "Espacio para personas con discapacidad"
        }
        response = await client.post("/accessibilidad/", json=feature_payload)
        assert response.status_code == 201


@pytest.mark.asyncio
async def test_list_accessibility_features(client: AsyncClient):
    """Test listar todas las características de accesibilidad"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "333444555",
        "name": "Features List Restaurant",
        "address": "789 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear múltiples características
    feature_names = ["Rampa de acceso", "Ascensor", "Menú en braille"]
    for name in feature_names:
        feature_payload = {
            "establishment_id": establishment_id,
            "name": name
        }
        await client.post("/accessibilidad/", json=feature_payload)
    
    # Listar características
    response = await client.get("/accessibilidad/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    
    # Verificar que las características creadas están en la lista
    names = [f["name"] for f in data]
    for name in feature_names:
        assert name in names


@pytest.mark.asyncio
async def test_get_accessibility_feature(client: AsyncClient):
    """Test obtener una característica específica"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "666777888",
        "name": "Get Feature Restaurant",
        "address": "321 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear característica
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Intérprete de señas",
        "description": "Servicio de interpretación disponible"
    }
    create_response = await client.post("/accessibilidad/", json=feature_payload)
    feature_id = create_response.json()["feature_id"]
    
    # Obtener característica
    response = await client.get(f"/accessibilidad/{feature_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feature_id
    assert data["name"] == "Intérprete de señas"
    assert data["description"] == "Servicio de interpretación disponible"
    assert data["establishment_id"] == establishment_id


@pytest.mark.asyncio
async def test_get_accessibility_feature_not_found(client: AsyncClient):
    """Test obtener característica inexistente debe fallar"""
    response = await client.get("/accessibilidad/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_accessibility_feature(client: AsyncClient):
    """Test actualizar una característica de accesibilidad"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "999888777",
        "name": "Update Feature Restaurant",
        "address": "654 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear característica
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Área de espera amplia",
        "description": "Descripción original"
    }
    create_response = await client.post("/accessibilidad/", json=feature_payload)
    feature_id = create_response.json()["feature_id"]
    
    # Actualizar característica
    update_payload = {
        "name": "Área de espera espaciosa",
        "description": "Zona amplia para sillas de ruedas"
    }
    response = await client.put(f"/accessibilidad/{feature_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == feature_id
    assert data["name"] == "Área de espera espaciosa"
    assert data["description"] == "Zona amplia para sillas de ruedas"


@pytest.mark.asyncio
async def test_update_accessibility_feature_partial(client: AsyncClient):
    """Test actualización parcial de característica"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123987456",
        "name": "Partial Update Restaurant",
        "address": "111 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear característica
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Mesa ajustable",
        "description": "Mesa de altura regulable"
    }
    create_response = await client.post("/accessibilidad/", json=feature_payload)
    feature_id = create_response.json()["feature_id"]
    
    # Actualizar solo la descripción
    update_payload = {
        "description": "Mesa con altura ajustable para sillas de ruedas"
    }
    response = await client.put(f"/accessibilidad/{feature_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mesa ajustable"  # No cambió
    assert data["description"] == "Mesa con altura ajustable para sillas de ruedas"


@pytest.mark.asyncio
async def test_update_accessibility_feature_duplicate_name(client: AsyncClient):
    """Test actualizar con nombre duplicado debe fallar"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "456789123",
        "name": "Duplicate Name Restaurant",
        "address": "222 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear dos características
    feature1_payload = {
        "establishment_id": establishment_id,
        "name": "Rampa",
        "description": "Acceso principal"
    }
    feature2_payload = {
        "establishment_id": establishment_id,
        "name": "Ascensor",
        "description": "Acceso a segundo piso"
    }
    
    create1_response = await client.post("/accessibilidad/", json=feature1_payload)
    create2_response = await client.post("/accessibilidad/", json=feature2_payload)
    feature2_id = create2_response.json()["feature_id"]
    
    # Intentar actualizar feature2 con el nombre de feature1
    update_payload = {
        "name": "Rampa"
    }
    response = await client.put(f"/accessibilidad/{feature2_id}", json=update_payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_accessibility_feature_not_found(client: AsyncClient):
    """Test actualizar característica inexistente debe fallar"""
    update_payload = {
        "name": "No existe"
    }
    response = await client.put("/accessibilidad/99999", json=update_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_accessibility_feature(client: AsyncClient):
    """Test eliminar una característica de accesibilidad"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "789456123",
        "name": "Delete Feature Restaurant",
        "address": "333 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear característica
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Característica a eliminar"
    }
    create_response = await client.post("/accessibilidad/", json=feature_payload)
    feature_id = create_response.json()["feature_id"]
    
    # Eliminar característica
    response = await client.delete(f"/accessibilidad/{feature_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verificar que fue eliminada
    get_response = await client.get(f"/accessibilidad/{feature_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_accessibility_feature_not_found(client: AsyncClient):
    """Test eliminar característica inexistente debe fallar"""
    response = await client.delete("/accessibilidad/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_accessibility_feature_without_description(client: AsyncClient):
    """Test crear característica sin descripción (campo opcional)"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "147258369",
        "name": "No Description Restaurant",
        "address": "444 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear característica sin descripción
    feature_payload = {
        "establishment_id": establishment_id,
        "name": "Entrada amplia"
    }
    response = await client.post("/accessibilidad/", json=feature_payload)
    assert response.status_code == 201
    
    # Verificar que se creó correctamente
    feature_id = response.json()["feature_id"]
    get_response = await client.get(f"/accessibilidad/{feature_id}")
    data = get_response.json()
    assert data["name"] == "Entrada amplia"
    assert data["description"] is None

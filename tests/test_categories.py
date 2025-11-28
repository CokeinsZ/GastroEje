import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    """Test crear una nueva categoría"""
    payload = {
        "name": "Italiana",
        "description": "Comida italiana tradicional"
    }
    
    response = await client.post("/categorias/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Italiana"
    assert data["description"] == "Comida italiana tradicional"
    assert "category_id" in data


@pytest.mark.asyncio
async def test_create_duplicate_category(client: AsyncClient):
    """Test crear una categoría duplicada debe fallar"""
    payload = {
        "name": "Mexicana",
        "description": "Comida mexicana"
    }
    
    # Crear primera vez
    await client.post("/categorias/", json=payload)
    
    # Intentar crear de nuevo
    response = await client.post("/categorias/", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_categories(client: AsyncClient):
    """Test listar todas las categorías"""
    # Crear algunas categorías
    categories = ["Japonesa", "China", "Tailandesa"]
    for cat_name in categories:
        await client.post("/categorias/", json={"name": cat_name})
    
    response = await client.get("/categorias/list")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 3


@pytest.mark.asyncio
async def test_get_category_by_id(client: AsyncClient):
    """Test obtener una categoría por ID"""
    # Crear categoría
    create_response = await client.post("/categorias/", json={
        "name": "Francesa",
        "description": "Alta cocina francesa"
    })
    created_data = create_response.json()
    category_id = created_data["category_id"]
    
    # Obtener categoría
    response = await client.get(f"/categorias/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == category_id
    assert data["name"] == "Francesa"


@pytest.mark.asyncio
async def test_get_category_not_found(client: AsyncClient):
    """Test obtener una categoría inexistente retorna 404"""
    response = await client.get("/categorias/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_category(client: AsyncClient):
    """Test actualizar una categoría"""
    # Crear categoría
    create_response = await client.post("/categorias/", json={
        "name": "Española",
        "description": "Tapas y paellas"
    })
    created_data = create_response.json()
    category_id = created_data["category_id"]
    
    # Actualizar categoría
    update_payload = {
        "name": "Española Premium",
        "description": "Lo mejor de España"
    }
    response = await client.put(f"/categorias/{category_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Española Premium"
    assert data["description"] == "Lo mejor de España"


@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient):
    """Test eliminar una categoría"""
    # Crear categoría
    create_response = await client.post("/categorias/", json={
        "name": "Temporal",
        "description": "Categoría temporal"
    })
    created_data = create_response.json()
    category_id = created_data["category_id"]
    
    # Eliminar categoría
    response = await client.delete(f"/categorias/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que fue eliminada
    get_response = await client.get(f"/categorias/{category_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_search_categories_by_name(client: AsyncClient):
    """Test buscar categorías por nombre"""
    # Crear categorías
    await client.post("/categorias/", json={"name": "Vegetariana"})
    await client.post("/categorias/", json={"name": "Vegana"})
    await client.post("/categorias/", json={"name": "Sin Gluten"})
    
    # Buscar categorías que contengan "veg"
    response = await client.get("/categorias/search/veg")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    # Debe encontrar al menos Vegetariana y Vegana
    assert len(data["items"]) >= 2


@pytest.mark.asyncio
async def test_add_category_to_establishment(client: AsyncClient):
    """Test asociar una categoría a un establecimiento"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "111222333",
        "name": "Restaurante Categoría Test",
        "address": "123 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Gourmet",
        "description": "Alta cocina"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Asociar categoría al establecimiento
    response = await client.post(f"/categorias/establecimiento/{establishment_id}/categoria/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que la categoría está asociada
    est_response = await client.get(f"/categorias/{category_id}/establecimientos")
    assert est_response.status_code == 200
    establishments = est_response.json()
    assert len(establishments) >= 1
    assert any(e["establishment_id"] == establishment_id for e in establishments)


@pytest.mark.asyncio
async def test_remove_category_from_establishment(client: AsyncClient):
    """Test desasociar una categoría de un establecimiento"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "444555666",
        "name": "Restaurante Remove Cat",
        "address": "456 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Casual Dining"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Asociar categoría al establecimiento
    await client.post(f"/categorias/establecimiento/{establishment_id}/categoria/{category_id}")
    
    # Desasociar categoría del establecimiento
    response = await client.delete(f"/categorias/establecimiento/{establishment_id}/categoria/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que la categoría fue eliminada
    est_response = await client.get(f"/categorias/{category_id}/establecimientos")
    establishments = est_response.json()
    assert not any(e["establishment_id"] == establishment_id for e in establishments)


@pytest.mark.asyncio
async def test_get_establishments_by_category(client: AsyncClient):
    """Test obtener todos los establecimientos de una categoría"""
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Fast Food",
        "description": "Comida rápida"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Crear múltiples establecimientos
    establishments_data = [
        {"NIT": "111111111", "name": "Fast Food 1", "address": "111 St", "opening_hour": "08:00:00", "closing_hour": "22:00:00"},
        {"NIT": "222222222", "name": "Fast Food 2", "address": "222 St", "opening_hour": "08:00:00", "closing_hour": "22:00:00"},
        {"NIT": "333333333", "name": "Fast Food 3", "address": "333 St", "opening_hour": "08:00:00", "closing_hour": "22:00:00"}
    ]
    
    establishment_ids = []
    for est_data in establishments_data:
        est_response = await client.post("/establishments/", json=est_data)
        establishment_ids.append(est_response.json()["establishment_id"])
    
    # Asociar todos los establecimientos a la categoría
    for est_id in establishment_ids:
        await client.post(f"/categorias/establecimiento/{est_id}/categoria/{category_id}")
    
    # Obtener establecimientos de la categoría
    response = await client.get(f"/categorias/{category_id}/establecimientos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_add_category_to_dish(client: AsyncClient):
    """Test asociar una categoría a un plato"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "777888999",
        "name": "Dish Category Restaurant",
        "address": "789 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Cat Test"
    }
    menu_response = await client.post(f"/menu/{est_data['establishment_id']}", json=menu_payload)
    menu_data = menu_response.json()
    
    # Crear plato
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Lasagna",
        "price": 15.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Pasta"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Asociar categoría al plato
    response = await client.post(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que la categoría está asociada
    dishes_response = await client.get(f"/categorias/{category_id}/platos")
    assert dishes_response.status_code == 200
    dishes = dishes_response.json()
    assert len(dishes) >= 1
    assert any(d["dish_id"] == dish_id for d in dishes)


@pytest.mark.asyncio
async def test_remove_category_from_dish(client: AsyncClient):
    """Test desasociar una categoría de un plato"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "123123123",
        "name": "Remove Dish Cat Restaurant",
        "address": "321 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Remove Cat"
    }
    menu_response = await client.post(f"/menu/{est_data['establishment_id']}", json=menu_payload)
    menu_data = menu_response.json()
    
    # Crear plato
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Spaghetti",
        "price": 12.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Carbohidratos"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Asociar categoría al plato
    await client.post(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    
    # Desasociar categoría del plato
    response = await client.delete(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que la categoría fue eliminada
    dishes_response = await client.get(f"/categorias/{category_id}/platos")
    dishes = dishes_response.json()
    assert not any(d["dish_id"] == dish_id for d in dishes)


@pytest.mark.asyncio
async def test_get_dishes_by_category(client: AsyncClient):
    """Test obtener todos los platos de una categoría"""
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Postres",
        "description": "Dulces y postres"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "999888777",
        "name": "Dessert Restaurant",
        "address": "999 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Postres"
    }
    menu_response = await client.post(f"/menu/{est_data['establishment_id']}", json=menu_payload)
    menu_data = menu_response.json()
    
    # Crear múltiples platos
    desserts = ["Tiramisu", "Cheesecake", "Flan"]
    dish_ids = []
    for dessert_name in desserts:
        dish_payload = {
            "menu_id": menu_data["menu_id"],
            "name": dessert_name,
            "price": 6.99
        }
        dish_response = await client.post("/platos/", json=dish_payload)
        dish_ids.append(dish_response.json()["dish_id"])
    
    # Asociar todos los platos a la categoría
    for dish_id in dish_ids:
        await client.post(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    
    # Obtener platos de la categoría
    response = await client.get(f"/categorias/{category_id}/platos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    dish_names = [d["name"] for d in data]
    for name in desserts:
        assert name in dish_names


@pytest.mark.asyncio
async def test_get_dishes_by_category_empty(client: AsyncClient):
    """Test obtener platos de una categoría sin platos"""
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Sin Platos"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Obtener platos (debería estar vacío)
    response = await client.get(f"/categorias/{category_id}/platos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_add_duplicate_category_to_establishment(client: AsyncClient):
    """Test intentar agregar la misma categoría dos veces a un establecimiento"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "555666777",
        "name": "Duplicate Cat Est",
        "address": "555 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Premium"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Asociar categoría al establecimiento (primera vez)
    await client.post(f"/categorias/establecimiento/{establishment_id}/categoria/{category_id}")
    
    # Intentar asociar la misma categoría nuevamente
    response = await client.post(f"/categorias/establecimiento/{establishment_id}/categoria/{category_id}")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_duplicate_category_to_dish(client: AsyncClient):
    """Test intentar agregar la misma categoría dos veces a un plato"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "888999000",
        "name": "Duplicate Cat Dish",
        "address": "888 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Duplicate"
    }
    menu_response = await client.post(f"/menu/{est_data['establishment_id']}", json=menu_payload)
    menu_data = menu_response.json()
    
    # Crear plato
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Pizza Margarita",
        "price": 10.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Pizza"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Asociar categoría al plato (primera vez)
    await client.post(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    
    # Intentar asociar la misma categoría nuevamente
    response = await client.post(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    assert response.status_code == 400

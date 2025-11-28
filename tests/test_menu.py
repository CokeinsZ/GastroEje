import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_menu(client: AsyncClient):
    """Test crear un nuevo menú"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123456789",
        "name": "Menu Test Restaurant",
        "address": "123 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu Principal"
    }
    response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Menu Principal"
    assert data["establishment_id"] == establishment_id
    assert "menu_id" in data


@pytest.mark.asyncio
async def test_create_menu_establishment_not_found(client: AsyncClient):
    """Test crear menú para establecimiento inexistente debe fallar"""
    menu_payload = {
        "establishment_id": 99999,
        "title": "Menu Invalido"
    }
    response = await client.post("/menu/99999", json=menu_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_menus_by_establishment(client: AsyncClient):
    """Test obtener todos los menús de un establecimiento"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "987654321",
        "name": "Multi Menu Restaurant",
        "address": "456 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear múltiples menús
    menu_titles = ["Desayuno", "Almuerzo", "Cena"]
    for title in menu_titles:
        menu_payload = {
            "establishment_id": establishment_id,
            "title": title
        }
        await client.post(f"/menu/{establishment_id}", json=menu_payload)
    
    # Obtener menús del establecimiento
    response = await client.get(f"/menu/establecimiento/{establishment_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    titles = [m["title"] for m in data]
    for title in menu_titles:
        assert title in titles


@pytest.mark.asyncio
async def test_get_dishes_by_menu(client: AsyncClient):
    """Test obtener todos los platos de un menú"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "111222333",
        "name": "Dishes Menu Restaurant",
        "address": "789 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu con Platos"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear platos en el menú
    dish_names = ["Hamburguesa", "Pizza", "Ensalada"]
    for dish_name in dish_names:
        dish_payload = {
            "menu_id": menu_id,
            "name": dish_name,
            "price": 10.99
        }
        await client.post("/platos/", json=dish_payload)
    
    # Obtener platos del menú
    response = await client.get(f"/menu/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    names = [d["name"] for d in data]
    for name in dish_names:
        assert name in names


@pytest.mark.asyncio
async def test_get_dishes_by_menu_not_found(client: AsyncClient):
    """Test obtener platos de menú inexistente debe fallar"""
    response = await client.get("/menu/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_dish_from_menu(client: AsyncClient):
    """Test obtener un plato específico de un menú"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "444555666",
        "name": "Dish Detail Restaurant",
        "address": "321 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu Detail"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear plato
    dish_payload = {
        "menu_id": menu_id,
        "name": "Pasta Carbonara",
        "price": 12.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Obtener el plato del menú
    response = await client.get(f"/menu/{menu_id}/item/{dish_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["dish_id"] == dish_id
    assert data["name"] == "Pasta Carbonara"


@pytest.mark.asyncio
async def test_get_dish_from_menu_not_found(client: AsyncClient):
    """Test obtener plato inexistente de un menú debe fallar"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "777888999",
        "name": "Not Found Restaurant",
        "address": "654 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu Not Found"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Intentar obtener plato inexistente
    response = await client.get(f"/menu/{menu_id}/item/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_menu(client: AsyncClient):
    """Test actualizar un menú"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "123123123",
        "name": "Update Menu Restaurant",
        "address": "111 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu Original"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Actualizar menú
    update_payload = {
        "title": "Menu Actualizado"
    }
    response = await client.put(f"/menu/{menu_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Menu Actualizado"
    assert data["menu_id"] == menu_id


@pytest.mark.asyncio
async def test_update_menu_not_found(client: AsyncClient):
    """Test actualizar menú inexistente debe fallar"""
    update_payload = {
        "title": "Menu No Existe"
    }
    response = await client.put("/menu/99999", json=update_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_menu(client: AsyncClient):
    """Test eliminar un menú"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "456456456",
        "name": "Delete Menu Restaurant",
        "address": "222 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu a Eliminar"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Eliminar menú
    response = await client.delete(f"/menu/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verificar que fue eliminado
    get_response = await client.get(f"/menu/{menu_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_menu_not_found(client: AsyncClient):
    """Test eliminar menú inexistente debe fallar"""
    response = await client.delete("/menu/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_dishes_by_menu_and_category(client: AsyncClient):
    """Test obtener platos de un menú filtrados por categoría"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "789789789",
        "name": "Category Filter Restaurant",
        "address": "333 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu con Categorias"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Entradas"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Crear platos
    entradas = ["Bruschetta", "Calamares", "Croquetas"]
    dish_ids = []
    for entrada in entradas:
        dish_payload = {
            "menu_id": menu_id,
            "name": entrada,
            "price": 8.99
        }
        dish_response = await client.post("/platos/", json=dish_payload)
        dish_ids.append(dish_response.json()["dish_id"])
    
    # Crear un plato que NO es entrada
    other_dish_payload = {
        "menu_id": menu_id,
        "name": "Steak",
        "price": 25.99
    }
    await client.post("/platos/", json=other_dish_payload)
    
    # Asociar solo las entradas a la categoría
    for dish_id in dish_ids:
        await client.post(f"/categorias/plato/{dish_id}/categoria/{category_id}")
    
    # Obtener platos del menú filtrados por categoría
    response = await client.get(f"/menu/{menu_id}/categoria/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    names = [d["name"] for d in data]
    for name in entradas:
        assert name in names
    assert "Steak" not in names


@pytest.mark.asyncio
async def test_get_dishes_by_menu_and_category_empty(client: AsyncClient):
    """Test obtener platos de un menú por categoría cuando no hay platos"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "321321321",
        "name": "Empty Category Restaurant",
        "address": "444 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu Vacio"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear categoría
    cat_response = await client.post("/categorias/", json={
        "name": "Sin Platos"
    })
    cat_data = cat_response.json()
    category_id = cat_data["category_id"]
    
    # Obtener platos (debería estar vacío)
    response = await client.get(f"/menu/{menu_id}/categoria/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_get_empty_menu(client: AsyncClient):
    """Test obtener platos de un menú vacío"""
    # Crear establecimiento
    establishment_payload = {
        "NIT": "654654654",
        "name": "Empty Menu Restaurant",
        "address": "555 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    establishment_id = est_data["establishment_id"]
    
    # Crear menú sin platos
    menu_payload = {
        "establishment_id": establishment_id,
        "title": "Menu Sin Platos"
    }
    menu_response = await client.post(f"/menu/{establishment_id}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Obtener platos del menú vacío
    response = await client.get(f"/menu/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

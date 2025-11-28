import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_dish(client: AsyncClient):
    """Test crear un nuevo plato"""
    # Primero crear un establecimiento
    establishment_payload = {
        "NIT": "123456789",
        "name": "Test Restaurant",
        "address": "123 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    # Crear un menú
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Principal"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear el plato
    dish_payload = {
        "menu_id": menu_id,
        "name": "Hamburguesa",
        "description": "Deliciosa hamburguesa",
        "price": 15.99,
        "img": "http://example.com/burger.jpg"
    }
    
    response = await client.post("/platos/", json=dish_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Hamburguesa"
    assert data["price"] == 15.99
    assert "dish_id" in data


@pytest.mark.asyncio
async def test_create_dish_invalid_price(client: AsyncClient):
    """Test crear un plato con precio inválido"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "987654321",
        "name": "Invalid Price Restaurant",
        "address": "456 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Test"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    # Intentar crear plato con precio negativo
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Plato Inválido",
        "price": -5.0
    }
    
    response = await client.post("/platos/", json=dish_payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_dishes(client: AsyncClient):
    """Test listar todos los platos"""
    response = await client.get("/platos/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_dish_by_id(client: AsyncClient):
    """Test obtener un plato por ID"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "111222333",
        "name": "Get Dish Restaurant",
        "address": "789 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Get"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Pizza",
        "price": 12.50
    }
    create_response = await client.post("/platos/", json=dish_payload)
    created_data = create_response.json()
    dish_id = created_data["dish_id"]
    
    # Obtener el plato
    response = await client.get(f"/platos/{dish_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["dish_id"] == dish_id
    assert data["name"] == "Pizza"


@pytest.mark.asyncio
async def test_get_dish_not_found(client: AsyncClient):
    """Test obtener un plato inexistente retorna 404"""
    response = await client.get("/platos/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_dish(client: AsyncClient):
    """Test actualizar un plato"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "444555666",
        "name": "Update Dish Restaurant",
        "address": "321 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Update"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Ensalada",
        "price": 8.99
    }
    create_response = await client.post("/platos/", json=dish_payload)
    created_data = create_response.json()
    dish_id = created_data["dish_id"]
    
    # Actualizar el plato
    update_payload = {
        "name": "Ensalada César",
        "price": 10.99,
        "description": "Con aderezo césar"
    }
    response = await client.put(f"/platos/{dish_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ensalada César"
    assert data["price"] == 10.99
    assert data["description"] == "Con aderezo césar"


@pytest.mark.asyncio
async def test_delete_dish(client: AsyncClient):
    """Test eliminar un plato"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "777888999",
        "name": "Delete Dish Restaurant",
        "address": "654 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Delete"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Plato Temporal",
        "price": 5.99
    }
    create_response = await client.post("/platos/", json=dish_payload)
    created_data = create_response.json()
    dish_id = created_data["dish_id"]
    
    # Eliminar el plato
    response = await client.delete(f"/platos/{dish_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que fue eliminado
    get_response = await client.get(f"/platos/{dish_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_dishes_by_menu(client: AsyncClient):
    """Test obtener platos por menú"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "123123123",
        "name": "Menu Dishes Restaurant",
        "address": "111 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Especial"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear varios platos para este menú
    dishes = ["Tacos", "Burritos", "Quesadillas"]
    for dish_name in dishes:
        dish_payload = {
            "menu_id": menu_id,
            "name": dish_name,
            "price": 7.99
        }
        await client.post("/platos/", json=dish_payload)
    
    # Obtener platos del menú
    response = await client.get(f"/platos/menu/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


@pytest.mark.asyncio
async def test_get_dishes_price_gt(client: AsyncClient):
    """Test obtener platos con precio mayor a un valor"""
    # Crear establecimiento y menú
    establishment_payload = {
        "NIT": "456456456",
        "name": "Price Filter Restaurant",
        "address": "222 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Prices"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    menu_id = menu_data["menu_id"]
    
    # Crear platos con diferentes precios
    dishes_prices = [5.99, 15.99, 25.99]
    for price in dishes_prices:
        dish_payload = {
            "menu_id": menu_id,
            "name": f"Plato ${price}",
            "price": price
        }
        await client.post("/platos/", json=dish_payload)
    
    # Obtener platos con precio mayor a 10
    response = await client.get("/platos/filter/price?min_price=10")
    assert response.status_code == 200
    data = response.json()
    # Al menos debería haber 2 platos (15.99 y 25.99)
    expensive_dishes = [d for d in data if d["price"] > 10]
    assert len(expensive_dishes) >= 2


@pytest.mark.asyncio
async def test_add_allergen_to_dish(client: AsyncClient):
    """Test asociar un alérgeno a un plato"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "789789789",
        "name": "Allergen Dish Restaurant",
        "address": "333 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Allergen"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Pasta Carbonara",
        "price": 14.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear alérgeno
    allergen_response = await client.post("/allergen/", json={"name": "Lácteos"})
    allergen_data = allergen_response.json()
    allergen_id = allergen_data["allergen_id"]
    
    # Asociar alérgeno al plato
    response = await client.post(f"/platos/{dish_id}/alergenos/{allergen_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que el alérgeno está asociado
    allergens_response = await client.get(f"/platos/{dish_id}/alergenos")
    assert allergens_response.status_code == 200
    allergens = allergens_response.json()
    assert len(allergens) >= 1
    assert any(a["allergen_id"] == allergen_id for a in allergens)


@pytest.mark.asyncio
async def test_remove_allergen_from_dish(client: AsyncClient):
    """Test desasociar un alérgeno de un plato"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "321321321",
        "name": "Remove Allergen Restaurant",
        "address": "444 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Remove"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Pastel de Chocolate",
        "price": 6.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear alérgeno
    allergen_response = await client.post("/allergen/", json={"name": "Cacao"})
    allergen_data = allergen_response.json()
    allergen_id = allergen_data["allergen_id"]
    
    # Asociar alérgeno al plato
    await client.post(f"/platos/{dish_id}/alergenos/{allergen_id}")
    
    # Desasociar alérgeno del plato
    response = await client.delete(f"/platos/{dish_id}/alergenos/{allergen_id}")
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
    
    # Verificar que el alérgeno fue eliminado
    allergens_response = await client.get(f"/platos/{dish_id}/alergenos")
    allergens = allergens_response.json()
    assert not any(a["allergen_id"] == allergen_id for a in allergens)


@pytest.mark.asyncio
async def test_get_allergens_by_dish(client: AsyncClient):
    """Test obtener todos los alérgenos de un plato"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "654654654",
        "name": "Get Allergens Restaurant",
        "address": "555 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Allergens"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Sushi Roll",
        "price": 18.99
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear múltiples alérgenos
    allergens_to_create = ["Pescado", "Soja", "Sésamo"]
    allergen_ids = []
    for allergen_name in allergens_to_create:
        allergen_response = await client.post("/allergen/", json={"name": allergen_name})
        allergen_ids.append(allergen_response.json()["allergen_id"])
    
    # Asociar todos los alérgenos al plato
    for allergen_id in allergen_ids:
        await client.post(f"/platos/{dish_id}/alergenos/{allergen_id}")
    
    # Obtener los alérgenos del plato
    response = await client.get(f"/platos/{dish_id}/alergenos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    allergen_names = [a["name"] for a in data]
    for name in allergens_to_create:
        assert name in allergen_names


@pytest.mark.asyncio
async def test_get_allergens_by_dish_empty(client: AsyncClient):
    """Test obtener alérgenos de un plato sin alérgenos"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "147147147",
        "name": "No Allergens Restaurant",
        "address": "666 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Clean"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Agua Mineral",
        "price": 2.50
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Obtener alérgenos (debería estar vacío)
    response = await client.get(f"/platos/{dish_id}/alergenos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_add_duplicate_allergen_to_dish(client: AsyncClient):
    """Test intentar agregar el mismo alérgeno dos veces a un plato"""
    # Crear establecimiento, menú y plato
    establishment_payload = {
        "NIT": "258258258",
        "name": "Duplicate Allergen Restaurant",
        "address": "777 Test St",
        "opening_hour": "08:00:00",
        "closing_hour": "22:00:00"
    }
    est_response = await client.post("/establishments/", json=establishment_payload)
    est_data = est_response.json()
    
    menu_payload = {
        "establishment_id": est_data["establishment_id"],
        "title": "Menu Duplicate"
    }
    menu_response = await client.post(f"/menu/{est_data["establishment_id"]}", json=menu_payload)
    menu_data = menu_response.json()
    
    dish_payload = {
        "menu_id": menu_data["menu_id"],
        "name": "Pan con Mantequilla",
        "price": 3.50
    }
    dish_response = await client.post("/platos/", json=dish_payload)
    dish_data = dish_response.json()
    dish_id = dish_data["dish_id"]
    
    # Crear alérgeno
    allergen_response = await client.post("/allergen/", json={"name": "Mantequilla"})
    allergen_data = allergen_response.json()
    allergen_id = allergen_data["allergen_id"]
    
    # Asociar alérgeno al plato (primera vez)
    await client.post(f"/platos/{dish_id}/alergenos/{allergen_id}")
    
    # Intentar asociar el mismo alérgeno nuevamente
    response = await client.post(f"/platos/{dish_id}/alergenos/{allergen_id}")
    assert response.status_code == 400

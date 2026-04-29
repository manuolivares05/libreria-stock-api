 
def test_crear_categoria(client):
    r = client.post("/api/v1/categorias", json={
        "nombre": "Literatura",
        "descripcion": "Ficción y no ficción"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["nombre"] == "Literatura"
    assert data["id"] is not None
 
 
def test_crear_categoria_duplicada(client, categoria):
    r = client.post("/api/v1/categorias", json={"nombre": "Técnico"})
    assert r.status_code == 409
 
 
def test_listar_categorias(client, categoria):
    r = client.get("/api/v1/categorias")
    assert r.status_code == 200
    assert len(r.json()) >= 1
 
 
def test_obtener_categoria_por_id(client, categoria):
    r = client.get(f"/api/v1/categorias/{categoria['id']}")
    assert r.status_code == 200
    assert r.json()["nombre"] == "Técnico"
 
 
def test_obtener_categoria_inexistente(client):
    r = client.get("/api/v1/categorias/9999")
    assert r.status_code == 404
 
 
def test_actualizar_categoria(client, categoria):
    r = client.patch(f"/api/v1/categorias/{categoria['id']}", json={
        "descripcion": "Nueva descripción"
    })
    assert r.status_code == 200
    assert r.json()["descripcion"] == "Nueva descripción"
    # El nombre no debe haber cambiado
    assert r.json()["nombre"] == "Técnico"
 
 
def test_eliminar_categoria(client, categoria):
    r = client.delete(f"/api/v1/categorias/{categoria['id']}")
    assert r.status_code == 204
    # Verificar que ya no existe
    r = client.get(f"/api/v1/categorias/{categoria['id']}")
    assert r.status_code == 404
 
 
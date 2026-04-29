
def test_crear_producto(client, producto):
    assert producto["nombre"] == "Clean Code"
    assert producto["precio"] == "3500.00"
    assert producto["id"] is not None
 
 
def test_crear_producto_crea_stock(client, producto):
    """Al crear un producto se debe crear automáticamente su registro de stock."""
    r = client.get(f"/api/v1/stock/producto/{producto['id']}")
    assert r.status_code == 200
    data = r.json()
    assert data["cantidad_actual"] == 0
    assert data["stock_minimo"] == 5
 
 
def test_crear_producto_isbn_duplicado(client, producto, categoria, proveedor):
    r = client.post("/api/v1/productos", json={
        "nombre": "Otro libro",
        "precio": 1000.00,
        "isbn": "9780132350884",  # mismo ISBN
        "id_categoria": categoria["id"],
        "id_proveedor": proveedor["id"]
    })
    assert r.status_code == 409
 
 
def test_crear_producto_precio_negativo(client, categoria, proveedor):
    r = client.post("/api/v1/productos", json={
        "nombre": "Producto inválido",
        "precio": -100.00,
        "id_categoria": categoria["id"],
        "id_proveedor": proveedor["id"]
    })
    assert r.status_code == 422
 
 
def test_obtener_producto_con_relaciones(client, producto):
    r = client.get(f"/api/v1/productos/{producto['id']}")
    assert r.status_code == 200
    data = r.json()
    assert data["categoria"] is not None
    assert data["proveedor"] is not None
 
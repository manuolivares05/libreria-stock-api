
def test_crear_venta_exitosa(client, producto_con_stock):
    """Flujo completo: venta → detalle → movimiento → stock actualizado."""
    producto_id = producto_con_stock["id"]
 
    r = client.post("/api/v1/ventas", json={
        "items": [{"id_producto": producto_id, "cantidad": 3}]
    })
    assert r.status_code == 201
    data = r.json()
 
    # Verificar estructura de la respuesta
    assert data["id"] is not None
    assert data["total"] == "10500.00"   # 3500 * 3
    assert len(data["detalles"]) == 1
 
    detalle = data["detalles"][0]
    assert detalle["cantidad"] == 3
    assert detalle["precio_unitario"] == "3500.00"
    assert detalle["subtotal"] == "10500.00"
 
 
def test_venta_descuenta_stock(client, producto_con_stock):
    """Después de una venta el stock debe bajar exactamente lo vendido."""
    producto_id = producto_con_stock["id"]
 
    # Stock inicial = 50
    r = client.get(f"/api/v1/stock/producto/{producto_id}")
    stock_inicial = r.json()["cantidad_actual"]
    assert stock_inicial == 50
 
    # Vender 5
    client.post("/api/v1/ventas", json={
        "items": [{"id_producto": producto_id, "cantidad": 5}]
    })
 
    # Stock debe ser 45
    r = client.get(f"/api/v1/stock/producto/{producto_id}")
    assert r.json()["cantidad_actual"] == 45
 
 
def test_venta_genera_movimiento_salida(client, producto_con_stock):
    """Toda venta debe generar un movimiento de tipo 'salida'."""
    producto_id = producto_con_stock["id"]
 
    client.post("/api/v1/ventas", json={
        "items": [{"id_producto": producto_id, "cantidad": 2}]
    })
 
    r = client.get(f"/api/v1/movimientos/producto/{producto_id}")
    movimientos = r.json()
 
    # Debe haber 2 movimientos: la entrada del fixture + esta salida
    salidas = [m for m in movimientos if m["tipo"] == "salida"]
    assert len(salidas) == 1
    assert salidas[0]["cantidad"] == 2
 
 
def test_venta_stock_insuficiente(client, producto_con_stock):
    """No se puede vender más de lo que hay en stock."""
    producto_id = producto_con_stock["id"]
 
    r = client.post("/api/v1/ventas", json={
        "items": [{"id_producto": producto_id, "cantidad": 999}]
    })
    assert r.status_code == 422
    assert "Stock insuficiente" in r.json()["detail"]
 
 
def test_venta_producto_inexistente(client):
    r = client.post("/api/v1/ventas", json={
        "items": [{"id_producto": 9999, "cantidad": 1}]
    })
    assert r.status_code == 404
 
 
def test_venta_items_vacios(client):
    r = client.post("/api/v1/ventas", json={"items": []})
    assert r.status_code == 422
 
 
def test_venta_productos_duplicados(client, producto_con_stock):
    """No se puede enviar el mismo producto dos veces en una venta."""
    producto_id = producto_con_stock["id"]
 
    r = client.post("/api/v1/ventas", json={
        "items": [
            {"id_producto": producto_id, "cantidad": 1},
            {"id_producto": producto_id, "cantidad": 2},
        ]
    })
    assert r.status_code == 422
 
 
def test_venta_multiples_productos(client, categoria, proveedor, producto_con_stock):
    """Una venta puede tener múltiples productos distintos."""
 
    # Crear segundo producto con stock
    r = client.post("/api/v1/productos", json={
        "nombre": "El Señor de los Anillos",
        "precio": 2800.00,
        "id_categoria": categoria["id"],
        "id_proveedor": proveedor["id"]
    })
    producto2_id = r.json()["id"]
    client.post("/api/v1/stock/entrada", json={
        "id_producto": producto2_id, "cantidad": 20
    })
 
    r = client.post("/api/v1/ventas", json={
        "items": [
            {"id_producto": producto_con_stock["id"], "cantidad": 2},
            {"id_producto": producto2_id,             "cantidad": 1},
        ]
    })
    assert r.status_code == 201
    data = r.json()
    assert len(data["detalles"]) == 2
    # Total = (3500*2) + (2800*1) = 9800
    assert data["total"] == "9800.00"
 
 
def test_stock_no_se_modifica_si_falla_venta(client, producto_con_stock):
    """
    Si la venta falla (stock insuficiente), el stock no debe cambiar.
    Valida que la transacción hace rollback correctamente.
    """
    producto_id = producto_con_stock["id"]
 
    stock_antes = client.get(f"/api/v1/stock/producto/{producto_id}").json()["cantidad_actual"]
 
    # Intentar venta que va a fallar
    client.post("/api/v1/ventas", json={
        "items": [{"id_producto": producto_id, "cantidad": 9999}]
    })
 
    stock_despues = client.get(f"/api/v1/stock/producto/{producto_id}").json()["cantidad_actual"]
 
    assert stock_antes == stock_despues  # no cambió
 
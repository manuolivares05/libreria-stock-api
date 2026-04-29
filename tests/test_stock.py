
def test_entrada_stock(client, producto):
    r = client.post("/api/v1/stock/entrada", json={
        "id_producto": producto["id"],
        "cantidad": 30
    })
    assert r.status_code == 201
    data = r.json()
    assert data["cantidad_actual"] == 30
    assert data["bajo_minimo"] is False
 
 
def test_entrada_stock_genera_movimiento(client, producto):
    """Toda entrada de stock debe registrar un movimiento tipo 'entrada'."""
    client.post("/api/v1/stock/entrada", json={
        "id_producto": producto["id"],
        "cantidad": 20
    })
    r = client.get(f"/api/v1/movimientos/producto/{producto['id']}")
    assert r.status_code == 200
    movimientos = r.json()
    assert len(movimientos) == 1
    assert movimientos[0]["tipo"] == "entrada"
    assert movimientos[0]["cantidad"] == 20
 
 
def test_entrada_cantidad_cero(client, producto):
    """No se puede cargar 0 unidades."""
    r = client.post("/api/v1/stock/entrada", json={
        "id_producto": producto["id"],
        "cantidad": 0
    })
    assert r.status_code == 422
 
 
def test_entrada_cantidad_negativa(client, producto):
    r = client.post("/api/v1/stock/entrada", json={
        "id_producto": producto["id"],
        "cantidad": -5
    })
    assert r.status_code == 422
 
 
def test_alerta_stock_bajo_minimo(client, producto):
    """
    Con cantidad_actual=0 y stock_minimo=5,
    el producto debe aparecer en alertas.
    """
    r = client.get("/api/v1/stock/alertas")
    assert r.status_code == 200
    alertas = r.json()
    ids = [a["id_producto"] for a in alertas]
    assert producto["id"] in ids
 
 
def test_actualizar_stock_minimo(client, producto):
    r = client.patch(f"/api/v1/stock/{producto['id']}/minimo", json={
        "stock_minimo": 10
    })
    assert r.status_code == 200
    assert r.json()["stock_minimo"] == 10
 
 
def test_stock_minimo_negativo(client, producto):
    r = client.patch(f"/api/v1/stock/{producto['id']}/minimo", json={
        "stock_minimo": -1
    })
    assert r.status_code == 422
 
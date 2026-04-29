# ============================================================
#  tests/conftest.py
#
#  Fixtures compartidas por todos los tests.
#  - Base de datos de test aislada
#  - Cliente HTTP que usa esa DB
#  - Datos de prueba reutilizables
# ============================================================
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parents[1] / ".env")

from app.config.database import Base, get_db
from app import create_app

# URL de la base de test
TEST_DB_URI = os.getenv(
    "TEST_DB_URI",
    "postgresql://postgres:1234@localhost:5432/libreria_test"
)

# Engine y sesión para tests
engine_test = create_engine(TEST_DB_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# Importar modelos para que Base los registre
from app.models.categoria     import Categoria      # noqa
from app.models.proveedor     import Proveedor       # noqa
from app.models.producto      import Producto        # noqa
from app.models.stock         import Stock           # noqa
from app.models.movimiento    import MovimientoStock # noqa
from app.models.venta         import Venta           # noqa
from app.models.detalle_venta import DetalleVenta    # noqa


@pytest.fixture(scope="session", autouse=True)
def crear_tablas():
    """Crea todas las tablas antes de correr los tests y las borra al final."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def db():
    """
    Sesión de DB por test. Hace rollback al terminar cada test
    para que los datos no persistan entre tests.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    """
    Cliente HTTP con la DB de test inyectada.
    Sobreescribe get_db() para que use la sesión de test.
    """
    os.environ["APP_CONTEXT"] = "testing"
    app = create_app()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ── Fixtures de datos ─────────────────────────────────────────────────────────

@pytest.fixture
def categoria(client):
    """Crea una categoría y la devuelve."""
    r = client.post("/api/v1/categorias", json={
        "nombre": "Técnico",
        "descripcion": "Libros de programación"
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def proveedor(client):
    """Crea un proveedor y lo devuelve."""
    r = client.post("/api/v1/proveedores", json={
        "nombre": "Editorial Test",
        "contacto": "test@editorial.com"
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def producto(client, categoria, proveedor):
    """Crea un producto con categoría y proveedor ya creados."""
    r = client.post("/api/v1/productos", json={
        "nombre": "Clean Code",
        "descripcion": "Robert C. Martin",
        "precio": 3500.00,
        "isbn": "9780132350884",
        "id_categoria": categoria["id"],
        "id_proveedor": proveedor["id"]
    })
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def producto_con_stock(client, producto):
    """Crea un producto y le carga 50 unidades de stock."""
    r = client.post("/api/v1/stock/entrada", json={
        "id_producto": producto["id"],
        "cantidad": 50
    })
    assert r.status_code == 201
    return producto
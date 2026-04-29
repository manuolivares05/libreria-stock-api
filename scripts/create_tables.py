# scripts/create_tables.py
#
# Crea las tablas en las tres bases de datos.
# Correr una sola vez, o cuando agregues nuevos modelos.
#
# Uso:
#   python scripts/create_tables.py

import sys
import os
from pathlib import Path

# Agregar la raíz del proyecto al path para que encuentre app/
sys.path.append(str(Path(__file__).parents[1]))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parents[1] / ".env")

from sqlalchemy import create_engine
from app.config.database import Base

# Importar todos los modelos para registrarlos en Base
from app.models.categoria     import Categoria      # noqa
from app.models.proveedor     import Proveedor       # noqa
from app.models.producto      import Producto        # noqa
from app.models.stock         import Stock           # noqa
from app.models.movimiento    import MovimientoStock # noqa
from app.models.venta         import Venta           # noqa
from app.models.detalle_venta import DetalleVenta    # noqa

BASES = {
    "development": os.getenv("DEV_DB_URI"),
    "testing":     os.getenv("TEST_DB_URI"),
    "production":  os.getenv("PROD_DB_URI"),
}

for entorno, url in BASES.items():
    if not url:
        print(f"  [skip]  {entorno} — URI no configurada en .env")
        continue
    try:
        engine = create_engine(url)
        Base.metadata.create_all(bind=engine)
        engine.dispose()
        print(f"  [ok]    {entorno} — tablas creadas en {url.split('@')[-1]}")
    except Exception as e:
        print(f"  [error] {entorno} — {e}")
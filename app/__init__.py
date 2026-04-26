from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
 
from app.config.config import get_config
from app.config import database
 
 
def create_app() -> FastAPI:
    cfg = get_config()
 
    # ── Lifespan (startup / shutdown) ─────────────────────────────────────
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # STARTUP
        _load_models()                        # registra ORM en Base
        database.init_db(cfg.DATABASE_URL)    # inicia engine con la URL correcta
        if cfg.DEBUG:
            database.create_tables()          # create_all solo en dev
        yield
        # SHUTDOWN
        database.dispose()
 
    # ── App ────────────────────────────────────────────────────────────────
    app = FastAPI(
        title=cfg.APP_NAME,
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs"  if cfg.DEBUG   else None,
        redoc_url="/redoc" if cfg.DEBUG  else None,
    )
 
    # ── Middleware ─────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
 
    @app.middleware("http")
    async def db_transaction_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        db = next(database.get_db())  # sesión directa, sin Depends
        request.state.db = db
        try:
            response = await call_next(request)
            db.commit() if response.status_code < 400 else db.rollback()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
        return response
 
    # ── Routers ────────────────────────────────────────────────────────────
    _register_routers(app)
 
    return app
 
 
def _load_models():
    """
    Importa todos los modelos para registrarlos en Base.
    Mismo patrón que importar los modelos en Flask antes del migrate.
    """
    from app.models import categoria      # noqa: F401
    from app.models import proveedor      # noqa: F401
    from app.models import producto       # noqa: F401
    from app.models import stock          # noqa: F401
    from app.models import movimiento     # noqa: F401
    from app.models import venta          # noqa: F401
    from app.models import detalle_venta  # noqa: F401
 
 
def _register_routers(app: FastAPI):
    from app.resources import (
        categorias, proveedores, productos,
        stock, movimientos, ventas, health,
    )
    PREFIX = "/api/v1"
    app.include_router(health.router)
    app.include_router(categorias.router,  prefix=PREFIX)
    app.include_router(proveedores.router, prefix=PREFIX)
    app.include_router(productos.router,   prefix=PREFIX)
    app.include_router(stock.router,       prefix=PREFIX)
    app.include_router(movimientos.router, prefix=PREFIX)
    app.include_router(ventas.router,      prefix=PREFIX)
 
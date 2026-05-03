from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
 
Base = declarative_base()
_engine = None
_SessionLocal = None
 
 
def init_db(database_url: str):
    """
    Inicializa el engine con la URL que venga de la config activa.
    Llamado desde create_app(), igual que db.init_app(app) en Flask.
    """
    global _engine, _SessionLocal
    _engine = create_engine(database_url, pool_pre_ping=True)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
 
 
def get_engine():
    return _engine
 
 
def create_tables():
    """Solo desarrollo. Producción usa Alembic."""
    Base.metadata.create_all(bind=_engine)
 
 
def dispose():
    if _engine:
        _engine.dispose()
 
 
def get_db():
    """Dependencia FastAPI — sesión por request."""
    db = _SessionLocal()
    try:
        yield db
        db.commit()       # ← commit al finalizar exitosamente
    except Exception:
        db.rollback()     # ← rollback si algo falla
        raise
    finally:
        db.close()
 
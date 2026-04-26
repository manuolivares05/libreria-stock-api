import os
from pathlib import Path
from pydantic_settings import BaseSettings
 
basedir = Path(__file__).parents[2]
 
 
class Config(BaseSettings):
    """
    Clase base. Valores compartidos por todos los entornos.
    Ningún entorno debería necesitar sobreescribir APP_NAME.
    """
    APP_NAME: str = "Librería Stock API"
    DEBUG:    bool = False
    TESTING:  bool = False
 
    # La URL de DB la define cada subclase según su variable de entorno
    DATABASE_URL: str = ""
 
    class Config:
        env_file = basedir / ".env"
        extra = "ignore"
 
 
class DevelopmentConfig(Config):
    """
    Entorno local de desarrollo.
    DEBUG=True activa: recarga automática, Swagger UI, create_all.
    Lee DEV_DB_URI del .env.
    """
    DEBUG:        bool = True
    DATABASE_URL: str  = os.getenv(
        "DEV_DB_URI",
        "postgresql://postgres:postgres@localhost:5432/libreria_dev"
    )
 
 
class TestingConfig(Config):
    """
    Entorno de tests automatizados.
    TESTING=True le indica a SQLAlchemy y a los tests
    que estamos en modo test (transacciones que no persisten, etc).
    Lee TEST_DB_URI del .env.
    """
    TESTING:      bool = True
    DEBUG:        bool = True
    DATABASE_URL: str  = os.getenv(
        "TEST_DB_URI",
        "postgresql://postgres:postgres@localhost:5432/libreria_test"
    )
 
 
class ProductionConfig(Config):
    """
    Entorno de producción.
    DEBUG=False: sin Swagger, sin create_all, sin recarga.
    Lee PROD_DB_URI del .env (obligatorio — sin default).
    """
    DEBUG:        bool = False
    DATABASE_URL: str  = os.getenv("PROD_DB_URI", "")
 
    class Config:
        env_file = basedir / ".env"
        extra = "ignore"
 
    def __init__(self, **data):
        super().__init__(**data)
        # En producción la URL no puede estar vacía.
        # Falla en el arranque, no en la primera query.
        if not self.DATABASE_URL:
            raise ValueError(
                "PROD_DB_URI no está configurada. "
                "Definila en el .env antes de levantar en producción."
            )
 
 
# ── Registro de configuraciones ───────────────────────────────────────────────
 
config = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}
 
 
def get_config() -> Config:
    """
    Lee APP_CONTEXT y devuelve la instancia de config correspondiente.
    Si APP_CONTEXT no está seteado, usa development.
 
    Uso:
        cfg = get_config()
        print(cfg.DATABASE_URL)   # URL del entorno activo
        print(cfg.DEBUG)          # True/False según entorno
    """
    env = os.getenv("APP_CONTEXT", "development")
    cfg_class = config.get(env, DevelopmentConfig)
    print(f"[config] Entorno activo: {env} → {cfg_class.__name__}")
    return cfg_class()
 
 
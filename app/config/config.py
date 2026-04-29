import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar el .env ANTES de leer cualquier variable
basedir = Path(__file__).parents[2]
load_dotenv(basedir / ".env")


class DevelopmentConfig:
    APP_NAME     = "Libreria Stock API"
    DEBUG        = True
    TESTING      = False
    DATABASE_URL = os.getenv("DEV_DB_URI", "postgresql://postgres:postgres@localhost:5432/libreria_dev")


class TestingConfig:
    APP_NAME     = "Libreria Stock API"
    DEBUG        = True
    TESTING      = True
    DATABASE_URL = os.getenv("TEST_DB_URI", "postgresql://postgres:postgres@localhost:5432/libreria_test")


class ProductionConfig:
    APP_NAME     = "Libreria Stock API"
    DEBUG        = False
    TESTING      = False
    DATABASE_URL = os.getenv("PROD_DB_URI", "")

    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("PROD_DB_URI no está configurada en el .env")


config = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}


def get_config():
    env = os.getenv("APP_CONTEXT", "development")
    cfg_class = config.get(env, DevelopmentConfig)
    print(f"[config] Entorno activo: {env} → {cfg_class.__name__}")
    instance = cfg_class()
    print(f"[config] DATABASE_URL: {instance.DATABASE_URL}")
    return instance
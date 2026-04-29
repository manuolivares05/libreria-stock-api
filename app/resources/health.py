from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.database import get_db
from app.config.config import get_config
 
router = APIRouter(tags=["Health"])
 
 
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
 
    return {
        "status": "ok",
        "app": get_config().APP_NAME,
        "database": db_status,
    }
 
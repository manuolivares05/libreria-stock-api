from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.movimiento_service import movimiento_service
from app.schemas.movimiento import MovimientoResponse
 
router = APIRouter(prefix="/movimientos", tags=["Movimientos"])
 
@router.get("/", response_model=list[MovimientoResponse])
def listar_movimientos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return movimiento_service.get_all(db, skip=skip, limit=limit)
 
@router.get("/producto/{id_producto}", response_model=list[MovimientoResponse])
def movimientos_por_producto(id_producto: int, db: Session = Depends(get_db)):
    return movimiento_service.get_por_producto(db, id_producto)
 
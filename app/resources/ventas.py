from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.venta_service import venta_service
from app.schemas.venta import VentaCreate, VentaResponse
 
router = APIRouter(prefix="/ventas", tags=["Ventas"])
 
@router.get("/", response_model=list[VentaResponse])
def listar_ventas(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return venta_service.get_all(db, skip=skip, limit=limit)
 
@router.get("/{id}", response_model=VentaResponse)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    return venta_service.get_by_id(db, id)
 
@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(schema: VentaCreate, db: Session = Depends(get_db)):
    """
    Registra una venta completa.
    Internamente: crea la venta, los detalles, los movimientos de stock
    y actualiza el stock. Todo en una sola transacción.
    """
    return venta_service.crear_venta(db, schema)
 
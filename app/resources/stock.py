from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.stock_service import stock_service
from app.schemas.schemas import StockResponse, StockUpdate, EntradaStockCreate
 
router = APIRouter(prefix="/stock", tags=["Stock"])
 
@router.get("/", response_model=list[StockResponse])
def listar_stock(db: Session = Depends(get_db)):
    return stock_service.get_all(db)
 
@router.get("/alertas", response_model=list[StockResponse])
def listar_alertas(db: Session = Depends(get_db)):
    """Devuelve productos cuyo stock actual está en o por debajo del mínimo."""
    return stock_service.get_alertas(db)
 
@router.get("/producto/{id_producto}", response_model=StockResponse)
def obtener_stock_producto(id_producto: int, db: Session = Depends(get_db)):
    return stock_service.get_por_producto(db, id_producto)
 
@router.post("/entrada", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def registrar_entrada(schema: EntradaStockCreate, db: Session = Depends(get_db)):
    """Registra entrada de mercadería. Genera movimiento tipo 'entrada' automáticamente."""
    return stock_service.registrar_entrada(db, schema)
 
@router.patch("/{id_producto}/minimo", response_model=StockResponse)
def actualizar_minimo(id_producto: int, schema: StockUpdate, db: Session = Depends(get_db)):
    return stock_service.actualizar_minimo(db, id_producto, schema)
 
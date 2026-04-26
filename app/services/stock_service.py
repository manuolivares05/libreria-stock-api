from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.movimiento import TipoMovimiento
from app.repository.stock_repository import stock_repository
from app.repository.movimiento_repository import movimiento_repository
from app.repository.producto_repository import producto_repository
from app.mapping.stock_mapper import stock_mapper
from app.mapping.movimiento_mapper import movimiento_mapper
from app.schemas.schemas import EntradaStockCreate, StockResponse, MovimientoResponse
 
 
class StockService:
 
    def get_all(self, db: Session) -> list[StockResponse]:
        orm_list = stock_repository.get_todos_con_producto(db)
        return stock_mapper.to_response_list(orm_list)
 
    def get_por_producto(self, db: Session, id_producto: int) -> StockResponse:
        orm_obj = stock_repository.get_por_producto(db, id_producto)
        if not orm_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe stock para el producto {id_producto}"
            )
        return stock_mapper.to_response(orm_obj)
 
    def get_alertas(self, db: Session) -> list[StockResponse]:
        orm_list = stock_repository.get_bajo_minimo(db)
        return stock_mapper.to_response_list(orm_list)
 
    def registrar_entrada(self, db: Session, schema: EntradaStockCreate) -> StockResponse:
        if not producto_repository.get(db, schema.id_producto):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {schema.id_producto} no encontrado"
            )
 
        movimiento_repository.registrar(
            db,
            id_producto=schema.id_producto,
            tipo=TipoMovimiento.entrada,
            cantidad=schema.cantidad,
        )
 
        stock = stock_repository.sumar_cantidad(db, schema.id_producto, schema.cantidad)
        return stock_mapper.to_response(stock)
 
 
stock_service = StockService()
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.movimiento import TipoMovimiento
from app.repository.stock_repository import stock_repository
from app.repository.movimiento_repository import movimiento_repository
from app.repository.producto_repository import producto_repository
from app.mapping.stock_mapper import stock_mapper
from app.schemas.stock import StockUpdate
from app.schemas.movimiento import EntradaStockCreate


class StockService:

    def get_all(self, db: Session):
        return stock_mapper.to_list(stock_repository.get_todos_con_producto(db))

    def get_por_producto(self, db: Session, id_producto: int):
        obj = stock_repository.get_por_producto(db, id_producto)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                f"No hay stock para producto {id_producto}")
        return stock_mapper.to_response(obj)

    def get_alertas(self, db: Session):
        return stock_mapper.to_list(stock_repository.get_bajo_minimo(db))

    def registrar_entrada(self, db: Session, schema: EntradaStockCreate):
        if not producto_repository.get(db, schema.id_producto):
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                f"Producto {schema.id_producto} no encontrado")
        movimiento_repository.registrar(
            db, schema.id_producto, TipoMovimiento.entrada, schema.cantidad
        )
        stock = stock_repository.sumar_cantidad(db, schema.id_producto, schema.cantidad)
        return stock_mapper.to_response(stock)

    def actualizar_minimo(self, db: Session, id_producto: int, schema: StockUpdate):
        obj = stock_repository.get_por_producto(db, id_producto)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                f"No hay stock para producto {id_producto}")
        obj.stock_minimo = schema.stock_minimo
        db.flush()
        return stock_mapper.to_response(obj)


stock_service = StockService()
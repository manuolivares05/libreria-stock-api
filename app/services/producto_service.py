from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.producto_repository import producto_repository
from app.mapping.producto_mapper import producto_mapper
from app.schemas.producto import ProductoCreate, ProductoUpdate


class ProductoService:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return producto_mapper.to_list(producto_repository.get_all(db, skip, limit))

    def get_by_id(self, db: Session, id: int):
        obj = producto_repository.get_con_relaciones(db, id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Producto {id} no encontrado")
        return producto_mapper.to_response(obj)

    def create(self, db: Session, schema: ProductoCreate):
        if schema.isbn and producto_repository.get_by_isbn(db, schema.isbn):
            raise HTTPException(status.HTTP_409_CONFLICT,
                                f"Ya existe un producto con ISBN {schema.isbn}")
        obj = producto_repository.create(db, schema)
        # Crear registro de stock vacío automáticamente
        from app.models.stock import Stock
        stock = Stock(id_producto=obj.id, cantidad_actual=0, stock_minimo=5)
        db.add(stock)
        db.flush()
        return producto_mapper.to_response(
            producto_repository.get_con_relaciones(db, obj.id)
        )

    def update(self, db: Session, id: int, schema: ProductoUpdate):
        obj = producto_repository.get(db, id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Producto {id} no encontrado")
        updated = producto_repository.update(db, obj, schema)
        return producto_mapper.to_response(
            producto_repository.get_con_relaciones(db, updated.id)
        )

    def delete(self, db: Session, id: int):
        if not producto_repository.get(db, id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Producto {id} no encontrado")
        producto_repository.delete(db, id)


producto_service = ProductoService()
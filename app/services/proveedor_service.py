from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.proveedor_repository import proveedor_repository
from app.mapping.proveedor_mapper import proveedor_mapper
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate


class ProveedorService:
    def get_all(self, db: Session):
        return proveedor_mapper.to_list(proveedor_repository.get_all(db))

    def get_by_id(self, db: Session, id: int):
        obj = proveedor_repository.get(db, id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Proveedor {id} no encontrado")
        return proveedor_mapper.to_response(obj)

    def create(self, db: Session, schema: ProveedorCreate):
        return proveedor_mapper.to_response(proveedor_repository.create(db, schema))

    def update(self, db: Session, id: int, schema: ProveedorUpdate):
        obj = proveedor_repository.get(db, id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Proveedor {id} no encontrado")
        return proveedor_mapper.to_response(proveedor_repository.update(db, obj, schema))

    def delete(self, db: Session, id: int):
        if not proveedor_repository.get(db, id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Proveedor {id} no encontrado")
        proveedor_repository.delete(db, id)


proveedor_service = ProveedorService()
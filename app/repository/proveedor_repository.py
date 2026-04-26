from sqlalchemy.orm import Session
from app.models.proveedor import Proveedor
from app.schemas.schemas import ProveedorCreate, ProveedorUpdate
from app.repository.base_repository import BaseRepository
 
 
class ProveedorRepository(BaseRepository[Proveedor, ProveedorCreate, ProveedorUpdate]):
 
    def get_by_nombre(self, db: Session, nombre: str) -> Proveedor | None:
        return db.query(Proveedor).filter(Proveedor.nombre == nombre).first()
 
 
proveedor_repository = ProveedorRepository(Proveedor)
 
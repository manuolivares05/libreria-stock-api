
from sqlalchemy.orm import Session, joinedload
from app.models.producto import Producto
from app.schemas.schemas import ProductoCreate, ProductoUpdate
from app.repository.base_repository import BaseRepository
 
 
class ProductoRepository(BaseRepository[Producto, ProductoCreate, ProductoUpdate]):
 
    def get_con_relaciones(self, db: Session, id: int) -> Producto | None:
        """
        joinedload hace un JOIN en la misma query en vez de N+1 queries.
        Úsalo cuando sabés que vas a necesitar categoria y proveedor.
        """
        return (
            db.query(Producto)
            .options(
                joinedload(Producto.categoria),
                joinedload(Producto.proveedor),
            )
            .filter(Producto.id == id)
            .first()
        )
 
    def get_by_isbn(self, db: Session, isbn: str) -> Producto | None:
        return db.query(Producto).filter(Producto.isbn == isbn).first()
 
    def get_by_categoria(self, db: Session, id_categoria: int) -> list[Producto]:
        return (
            db.query(Producto)
            .filter(Producto.id_categoria == id_categoria)
            .all()
        )
 
 
producto_repository = ProductoRepository(Producto)
 
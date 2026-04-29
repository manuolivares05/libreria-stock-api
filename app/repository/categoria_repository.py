from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate
from app.repository.base_repository import BaseRepository
 
 
class CategoriaRepository(BaseRepository[Categoria, CategoriaCreate, CategoriaUpdate]):
 
    def get_by_nombre(self, db: Session, nombre: str) -> Categoria | None:
        return db.query(Categoria).filter(Categoria.nombre == nombre).first()
 
 
categoria_repository = CategoriaRepository(Categoria)
 
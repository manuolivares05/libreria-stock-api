
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository.categoria_repository import categoria_repository
from app.schemas.schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse
 
 
class CategoriaService:
 
    def get_all(self, db: Session) -> list[CategoriaResponse]:
        return categoria_repository.get_all(db)
 
    def get_by_id(self, db: Session, id: int) -> CategoriaResponse:
        categoria = categoria_repository.get(db, id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría {id} no encontrada"
            )
        return categoria
 
    def create(self, db: Session, schema: CategoriaCreate) -> CategoriaResponse:
        # Verificar nombre duplicado
        if categoria_repository.get_by_nombre(db, schema.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría con el nombre '{schema.nombre}'"
            )
        return categoria_repository.create(db, schema)
 
    def update(self, db: Session, id: int, schema: CategoriaUpdate) -> CategoriaResponse:
        categoria = self.get_by_id(db, id)
        return categoria_repository.update(db, categoria, schema)
 
    def delete(self, db: Session, id: int) -> None:
        self.get_by_id(db, id)  # lanza 404 si no existe
        categoria_repository.delete(db, id)
 
 
categoria_service = CategoriaService()
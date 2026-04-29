from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.categoria_service import categoria_service
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate, CategoriaResponse
 
router = APIRouter(prefix="/categorias", tags=["Categorías"])
 
@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return categoria_service.get_all(db)
 
@router.get("/{id}", response_model=CategoriaResponse)
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    return categoria_service.get_by_id(db, id)
 
@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(schema: CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_service.create(db, schema)
 
@router.patch("/{id}", response_model=CategoriaResponse)
def actualizar_categoria(id: int, schema: CategoriaUpdate, db: Session = Depends(get_db)):
    return categoria_service.update(db, id, schema)
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    categoria_service.delete(db, id)
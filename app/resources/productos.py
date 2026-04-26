from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.producto_service import producto_service
from app.schemas.schemas import ProductoCreate, ProductoUpdate, ProductoResponse
 
router = APIRouter(prefix="/productos", tags=["Productos"])
 
@router.get("/", response_model=list[ProductoResponse])
def listar_productos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return producto_service.get_all(db, skip=skip, limit=limit)
 
@router.get("/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    return producto_service.get_by_id(db, id)
 
@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(schema: ProductoCreate, db: Session = Depends(get_db)):
    return producto_service.create(db, schema)
 
@router.patch("/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, schema: ProductoUpdate, db: Session = Depends(get_db)):
    return producto_service.update(db, id, schema)
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto_service.delete(db, id)
 
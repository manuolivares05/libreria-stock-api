from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.proveedor_service import proveedor_service
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorResponse
 
router = APIRouter(prefix="/proveedores", tags=["Proveedores"])
 
@router.get("/", response_model=list[ProveedorResponse])
def listar_proveedores(db: Session = Depends(get_db)):
    return proveedor_service.get_all(db)
 
@router.get("/{id}", response_model=ProveedorResponse)
def obtener_proveedor(id: int, db: Session = Depends(get_db)):
    return proveedor_service.get_by_id(db, id)
 
@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def crear_proveedor(schema: ProveedorCreate, db: Session = Depends(get_db)):
    return proveedor_service.create(db, schema)
 
@router.patch("/{id}", response_model=ProveedorResponse)
def actualizar_proveedor(id: int, schema: ProveedorUpdate, db: Session = Depends(get_db)):
    return proveedor_service.update(db, id, schema)
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proveedor(id: int, db: Session = Depends(get_db)):
    proveedor_service.delete(db, id)
 
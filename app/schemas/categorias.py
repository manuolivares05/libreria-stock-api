from typing import Optional
from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CategoriaCreate(BaseModel):
    nombre:      str
    descripcion: Optional[str] = None


class CategoriaUpdate(BaseModel):
    nombre:      Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaResponse(SchemaBase):
    id:          int
    nombre:      str
    descripcion: Optional[str] = None
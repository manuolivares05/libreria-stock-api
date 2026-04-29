from typing import Optional
from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProveedorCreate(BaseModel):
    nombre:   str
    contacto: Optional[str] = None


class ProveedorUpdate(BaseModel):
    nombre:   Optional[str] = None
    contacto: Optional[str] = None


class ProveedorResponse(SchemaBase):
    id:       int
    nombre:   str
    contacto: Optional[str] = None
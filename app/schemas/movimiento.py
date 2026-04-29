from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MovimientoResponse(SchemaBase):
    id:          int
    id_producto: int
    tipo:        str
    cantidad:    int
    fecha:       datetime


class EntradaStockCreate(BaseModel):
    id_producto: int
    cantidad:    int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        return v
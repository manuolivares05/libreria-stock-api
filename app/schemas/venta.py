from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict, field_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ItemVentaCreate(BaseModel):
    id_producto: int
    cantidad:    int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        return v


class VentaCreate(BaseModel):
    items: List[ItemVentaCreate]

    @field_validator("items")
    @classmethod
    def items_validos(cls, v: list) -> list:
        if not v:
            raise ValueError("La venta debe contener al menos un ítem")
        ids = [i.id_producto for i in v]
        if len(ids) != len(set(ids)):
            raise ValueError("No puede haber productos duplicados en una venta")
        return v


class DetalleVentaResponse(SchemaBase):
    id:              int
    id_producto:     int
    cantidad:        int
    precio_unitario: Decimal
    subtotal:        Decimal = Decimal("0")


class VentaResponse(SchemaBase):
    id:       int
    fecha:    datetime
    total:    Decimal
    detalles: List[DetalleVentaResponse] = []
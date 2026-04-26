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
    items: list[ItemVentaCreate]
 
    @field_validator("items")
    @classmethod
    def items_validos(cls, v: list) -> list:
        if not v:
            raise ValueError("La venta debe contener al menos un ítem")
        ids = [item.id_producto for item in v]
        if len(ids) != len(set(ids)):
            raise ValueError("No puede haber productos duplicados en una venta")
        return v
 
class DetalleVentaResponse(SchemaBase):
    id:              int
    id_producto:     int
    cantidad:        int
    precio_unitario: Decimal
    subtotal:        Decimal   # campo calculado, lo agrega el mapper
 
class VentaResponse(SchemaBase):
    id:       int
    fecha:    datetime
    total:    Decimal
    detalles: list[DetalleVentaResponse] = []
 
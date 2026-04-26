class ProductoBase(BaseModel):
    nombre:       str
    descripcion:  Optional[str]  = None
    precio:       Decimal
    isbn:         Optional[str]  = None
    id_categoria: int
    id_proveedor: int
 
    @field_validator("precio")
    @classmethod
    def precio_positivo(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v
 
class ProductoCreate(ProductoBase):
    pass
 
class ProductoUpdate(BaseModel):
    nombre:       Optional[str]     = None
    descripcion:  Optional[str]     = None
    precio:       Optional[Decimal] = None
    isbn:         Optional[str]     = None
    id_categoria: Optional[int]     = None
    id_proveedor: Optional[int]     = None
 
class ProductoResponse(SchemaBase):
    id:           int
    nombre:       str
    descripcion:  Optional[str]  = None
    precio:       Decimal
    isbn:         Optional[str]  = None
    id_categoria: int
    id_proveedor: int
    # Relaciones opcionales — se pueblan solo si el mapper las incluye
    categoria:    Optional[CategoriaResponse] = None
    proveedor:    Optional[ProveedorResponse] = None
 
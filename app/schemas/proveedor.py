class ProveedorBase(BaseModel):
    nombre:   str
    contacto: Optional[str] = None
 
class ProveedorCreate(ProveedorBase):
    pass
 
class ProveedorUpdate(BaseModel):
    nombre:   Optional[str] = None
    contacto: Optional[str] = None
 
class ProveedorResponse(SchemaBase):
    id:       int
    nombre:   str
    contacto: Optional[str] = None
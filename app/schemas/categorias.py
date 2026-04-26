class CategoriaBase(BaseModel):
    nombre:      str
    descripcion: Optional[str] = None
 
class CategoriaCreate(CategoriaBase):
    pass
 
class CategoriaUpdate(BaseModel):
    nombre:      Optional[str] = None
    descripcion: Optional[str] = None
 
class CategoriaResponse(SchemaBase):
    id:          int
    nombre:      str
    descripcion: Optional[str] = None
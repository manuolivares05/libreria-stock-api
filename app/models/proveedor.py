from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base
 
class Proveedor(Base):
    __tablename__ = "proveedores"
 
    id       = Column(Integer, primary_key=True, index=True)
    nombre   = Column(String(150), nullable=False)
    contacto = Column(String(200), nullable=True)
 
    productos = relationship("Producto", back_populates="proveedor")

from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
 
class Producto(Base):
    __tablename__ = "productos"
 
    id           = Column(Integer, primary_key=True, index=True)
    nombre       = Column(String(200), nullable=False)
    descripcion  = Column(Text, nullable=True)
    precio       = Column(Numeric(10, 2), nullable=False)
    isbn         = Column(String(20), unique=True, nullable=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
 
    # Relaciones
    categoria        = relationship("Categoria", back_populates="productos")
    proveedor        = relationship("Proveedor", back_populates="productos")
    stock            = relationship("Stock", back_populates="producto", uselist=False)
    movimientos      = relationship("MovimientoStock", back_populates="producto")
    detalles_venta   = relationship("DetalleVenta", back_populates="producto")

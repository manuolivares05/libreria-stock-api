from sqlalchemy import Column, Integer, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.config.database import Base
 
class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
 
    id              = Column(Integer, primary_key=True, index=True)
    id_venta        = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    id_producto     = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad        = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
 
    # Restricción: el mismo producto no puede aparecer dos veces en una venta
    __table_args__ = (
        UniqueConstraint("id_venta", "id_producto", name="uq_venta_producto"),
    )
 
    venta    = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")
 

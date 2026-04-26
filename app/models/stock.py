#  REGLA CLAVE: cantidad_actual nunca se modifica directamente
#  desde la aplicación. Solo el service de stock lo toca,
#  y siempre como consecuencia de un MovimientoStock.
# ============================================================
 
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
 
class Stock(Base):
    __tablename__ = "stock"
 
    id              = Column(Integer, primary_key=True, index=True)
    id_producto     = Column(Integer, ForeignKey("productos.id"), unique=True, nullable=False)
    cantidad_actual = Column(Integer, nullable=False, default=0)
    stock_minimo    = Column(Integer, nullable=False, default=5)
 
    producto = relationship("Producto", back_populates="stock")
 

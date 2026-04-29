from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base
 
class Venta(Base):
    __tablename__ = "ventas"
 
    id    = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
 
    detalles = relationship("DetalleVenta", back_populates="venta")
 

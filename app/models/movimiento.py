#  Esta tabla es el log de auditoría. Nunca se borran ni
#  editan registros de movimientos. Solo INSERT.
# ============================================================
 
import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base
 
class TipoMovimiento(str, enum.Enum):
    entrada = "entrada"
    salida  = "salida"
 
class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"
 
    id          = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo        = Column(Enum(TipoMovimiento), nullable=False)
    cantidad    = Column(Integer, nullable=False)
    # server_default=func.now() delega el timestamp al servidor de DB,
    # lo cual es más confiable que generarlo en Python
    fecha       = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
 
    producto = relationship("Producto", back_populates="movimientos")

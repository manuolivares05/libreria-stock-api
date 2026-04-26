from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
 
 
class VentaRepository:
 
    def crear_venta(self, db: Session, total: Decimal) -> Venta:
        venta = Venta(total=total)
        db.add(venta)
        db.flush()   # necesitamos venta.id antes de crear los detalles
        return venta
 
    def agregar_detalle(
        self,
        db: Session,
        id_venta: int,
        id_producto: int,
        cantidad: int,
        precio_unitario: Decimal,
    ) -> DetalleVenta:
        detalle = DetalleVenta(
            id_venta=id_venta,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )
        db.add(detalle)
        db.flush()
        return detalle
 
    def get_con_detalles(self, db: Session, id_venta: int) -> Venta | None:
        return (
            db.query(Venta)
            .options(joinedload(Venta.detalles))
            .filter(Venta.id == id_venta)
            .first()
        )
 
    def get_todas(self, db: Session, skip: int = 0, limit: int = 50) -> list[Venta]:
        return (
            db.query(Venta)
            .order_by(Venta.fecha.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
 
 
venta_repository = VentaRepository()
 
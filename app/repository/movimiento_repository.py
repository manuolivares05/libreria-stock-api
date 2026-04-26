 
from sqlalchemy.orm import Session
from app.models.movimiento import MovimientoStock, TipoMovimiento
 
 
class MovimientoRepository:
 
    def registrar(
        self,
        db: Session,
        id_producto: int,
        tipo: TipoMovimiento,
        cantidad: int,
    ) -> MovimientoStock:
        movimiento = MovimientoStock(
            id_producto=id_producto,
            tipo=tipo,
            cantidad=cantidad,
        )
        db.add(movimiento)
        db.flush()
        return movimiento
 
    def get_por_producto(
        self, db: Session, id_producto: int, limit: int = 50
    ) -> list[MovimientoStock]:
        return (
            db.query(MovimientoStock)
            .filter(MovimientoStock.id_producto == id_producto)
            .order_by(MovimientoStock.fecha.desc())
            .limit(limit)
            .all()
        )
 
    def get_todos(self, db: Session, skip: int = 0, limit: int = 100) -> list[MovimientoStock]:
        return (
            db.query(MovimientoStock)
            .order_by(MovimientoStock.fecha.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
 
 
movimiento_repository = MovimientoRepository()
 
 
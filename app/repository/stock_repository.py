from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.repository.base_repository import BaseRepository
 
 
class StockRepository(BaseRepository):
 
    def __init__(self):
        super().__init__(Stock)
 
    def get_por_producto(self, db: Session, id_producto: int) -> Stock | None:
        return db.query(Stock).filter(Stock.id_producto == id_producto).first()
 
    def get_todos_con_producto(self, db: Session) -> list[Stock]:
        """Para el endpoint GET /stock, carga el producto en el mismo query."""
        from sqlalchemy.orm import joinedload
        return db.query(Stock).options(joinedload(Stock.producto)).all()
 
    def get_bajo_minimo(self, db: Session) -> list[Stock]:
        """Devuelve todos los registros donde cantidad_actual <= stock_minimo."""
        return (
            db.query(Stock)
            .filter(Stock.cantidad_actual <= Stock.stock_minimo)
            .all()
        )
 
    def sumar_cantidad(self, db: Session, id_producto: int, cantidad: int) -> Stock:
        """
        Incrementa el stock (entrada de mercadería).
        Llamado exclusivamente desde stock_service tras registrar el movimiento.
        """
        stock = self.get_por_producto(db, id_producto)
        if not stock:
            raise ValueError(f"No existe registro de stock para producto {id_producto}")
        stock.cantidad_actual += cantidad
        db.flush()
        return stock
 
    def restar_cantidad(self, db: Session, id_producto: int, cantidad: int) -> Stock:
        """
        Decrementa el stock (salida por venta).
        Verifica que no quede negativo ANTES de modificar.
        Llamado exclusivamente desde stock_service.
        """
        stock = self.get_por_producto(db, id_producto)
        if not stock:
            raise ValueError(f"No existe registro de stock para producto {id_producto}")
        if stock.cantidad_actual < cantidad:
            raise ValueError(
                f"Stock insuficiente para producto {id_producto}. "
                f"Disponible: {stock.cantidad_actual}, solicitado: {cantidad}"
            )
        stock.cantidad_actual -= cantidad
        db.flush()
        return stock
 
 
stock_repository = StockRepository()
 
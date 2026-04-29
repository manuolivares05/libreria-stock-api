from sqlalchemy.orm import Session
from app.repository.movimiento_repository import movimiento_repository
from app.mapping.movimiento_mapper import movimiento_mapper


class MovimientoService:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return movimiento_mapper.to_list(movimiento_repository.get_todos(db, skip, limit))

    def get_por_producto(self, db: Session, id_producto: int):
        return movimiento_mapper.to_list(
            movimiento_repository.get_por_producto(db, id_producto)
        )


movimiento_service = MovimientoService()

from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.movimiento import TipoMovimiento
from app.repository.producto_repository import producto_repository
from app.repository.stock_repository import stock_repository
from app.repository.movimiento_repository import movimiento_repository
from app.repository.venta_repository import venta_repository
from app.mapping.venta_mapper import venta_mapper
from app.schemas.schemas import VentaCreate, VentaResponse
 
 
class VentaService:
 
    def crear_venta(self, db: Session, schema: VentaCreate) -> VentaResponse:
 
        # ── Validaciones previas (sin escribir nada aún) ───────────────────
        productos_cache = {}
 
        for item in schema.items:
            producto = producto_repository.get(db, item.id_producto)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto {item.id_producto} no encontrado"
                )
 
            stock = stock_repository.get_por_producto(db, item.id_producto)
            if not stock:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El producto '{producto.nombre}' no tiene registro de stock"
                )
            if stock.cantidad_actual < item.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=(
                        f"Stock insuficiente para '{producto.nombre}'. "
                        f"Disponible: {stock.cantidad_actual}, "
                        f"solicitado: {item.cantidad}"
                    )
                )
 
            productos_cache[item.id_producto] = producto
 
        # ── Calcular total ─────────────────────────────────────────────────
        total = sum(
            Decimal(str(productos_cache[item.id_producto].precio)) * item.cantidad
            for item in schema.items
        )
 
        # ── Escribir en DB ─────────────────────────────────────────────────
        venta = venta_repository.crear_venta(db, total)
 
        for item in schema.items:
            producto = productos_cache[item.id_producto]
 
            venta_repository.agregar_detalle(
                db,
                id_venta=venta.id,
                id_producto=item.id_producto,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,
            )
 
            movimiento_repository.registrar(
                db,
                id_producto=item.id_producto,
                tipo=TipoMovimiento.salida,
                cantidad=item.cantidad,
            )
 
            stock_repository.restar_cantidad(db, item.id_producto, item.cantidad)
 
        # ── Mapear respuesta ───────────────────────────────────────────────
        # Recargamos la venta con sus detalles para pasársela al mapper limpiamente
        venta_completa = venta_repository.get_con_detalles(db, venta.id)
        return venta_mapper.to_response(venta_completa)
 
    def get_all(self, db: Session, skip: int = 0, limit: int = 50) -> list[VentaResponse]:
        orm_list = venta_repository.get_todas(db, skip=skip, limit=limit)
        return venta_mapper.to_response_list(orm_list)
 
    def get_by_id(self, db: Session, id: int) -> VentaResponse:
        venta = venta_repository.get_con_detalles(db, id)
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta {id} no encontrada"
            )
        return venta_mapper.to_response(venta)
 
 
venta_service = VentaService()
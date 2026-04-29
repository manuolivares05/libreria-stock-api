from decimal import Decimal
from app.schemas.venta import VentaResponse, DetalleVentaResponse

class VentaMapper:
 
    @staticmethod
    def detalle_to_response(orm_detalle) -> DetalleVentaResponse:
        subtotal = (
            Decimal(str(orm_detalle.cantidad))
            * Decimal(str(orm_detalle.precio_unitario))
        )
        return DetalleVentaResponse(
            id=orm_detalle.id,
            id_producto=orm_detalle.id_producto,
            cantidad=orm_detalle.cantidad,
            precio_unitario=orm_detalle.precio_unitario,
            subtotal=subtotal,
        )
 
    @staticmethod
    def to_response(orm_venta) -> VentaResponse:
        detalles = [
            VentaMapper.detalle_to_response(d)
            for d in orm_venta.detalles
        ]
        return VentaResponse(
            id=orm_venta.id,
            fecha=orm_venta.fecha,
            total=orm_venta.total,
            detalles=detalles,
        )
 
    @staticmethod
    def to_response_list(orm_list: list) -> list[VentaResponse]:
        return [VentaMapper.to_response(v) for v in orm_list]
 
 
venta_mapper = VentaMapper()
 
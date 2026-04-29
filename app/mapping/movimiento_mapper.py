from app.schemas.movimiento import MovimientoResponse

class MovimientoMapper:
 
    @staticmethod
    def to_response(orm_obj) -> MovimientoResponse:
        return MovimientoResponse.model_validate(orm_obj)
 
    @staticmethod
    def to_list(orm_list: list) -> list:
        return [MovimientoMapper.to_response(o) for o in orm_list]
 
movimiento_mapper = MovimientoMapper()
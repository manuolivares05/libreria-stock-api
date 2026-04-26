class MovimientoMapper:
 
    @staticmethod
    def to_response(orm_obj) -> MovimientoResponse:
        return MovimientoResponse.model_validate(orm_obj)
 
    @staticmethod
    def to_response_list(orm_list: list) -> list[MovimientoResponse]:
        return [MovimientoMapper.to_response(obj) for obj in orm_list]
 
 
movimiento_mapper = MovimientoMapper()
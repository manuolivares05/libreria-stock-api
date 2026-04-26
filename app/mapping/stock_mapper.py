class StockMapper:
 
    @staticmethod
    def to_response(orm_obj) -> StockResponse:
        return StockResponse(
            id=orm_obj.id,
            id_producto=orm_obj.id_producto,
            cantidad_actual=orm_obj.cantidad_actual,
            stock_minimo=orm_obj.stock_minimo,
            bajo_minimo=orm_obj.cantidad_actual <= orm_obj.stock_minimo,
        )
 
    @staticmethod
    def to_response_list(orm_list: list) -> list[StockResponse]:
        return [StockMapper.to_response(obj) for obj in orm_list]
 
 
stock_mapper = StockMapper()
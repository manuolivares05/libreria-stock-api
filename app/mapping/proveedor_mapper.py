class ProveedorMapper:
 
    @staticmethod
    def to_response(orm_obj) -> ProveedorResponse:
        return ProveedorResponse.model_validate(orm_obj)
 
    @staticmethod
    def to_response_list(orm_list: list) -> list[ProveedorResponse]:
        return [ProveedorMapper.to_response(obj) for obj in orm_list]
 
 
proveedor_mapper = ProveedorMapper()
 
class CategoriaMapper:
 
    @staticmethod
    def to_response(orm_obj) -> CategoriaResponse:
        return CategoriaResponse.model_validate(orm_obj)
 
    @staticmethod
    def to_response_list(orm_list: list) -> list[CategoriaResponse]:
        return [CategoriaMapper.to_response(obj) for obj in orm_list]
 
 
categoria_mapper = CategoriaMapper()
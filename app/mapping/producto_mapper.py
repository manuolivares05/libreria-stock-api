class ProductoMapper:
 
    @staticmethod
    def to_response(orm_obj, include_relations: bool = True) -> ProductoResponse:
        data = {
            "id":           orm_obj.id,
            "nombre":       orm_obj.nombre,
            "descripcion":  orm_obj.descripcion,
            "precio":       orm_obj.precio,
            "isbn":         orm_obj.isbn,
            "id_categoria": orm_obj.id_categoria,
            "id_proveedor": orm_obj.id_proveedor,
        }
 
        if include_relations:
            # Solo intenta mapear relaciones si SQLAlchemy las cargó.
            # Acceder a una relación no cargada lanzaría una query extra
            # (problema N+1). Los endpoints que necesiten relaciones deben
            # usar get_con_relaciones() en el repository.
            try:
                data["categoria"] = CategoriaResponse.model_validate(orm_obj.categoria) \
                    if orm_obj.categoria else None
                data["proveedor"] = ProveedorResponse.model_validate(orm_obj.proveedor) \
                    if orm_obj.proveedor else None
            except Exception:
                data["categoria"] = None
                data["proveedor"] = None
 
        return ProductoResponse(**data)
 
    @staticmethod
    def to_response_list(orm_list: list) -> list[ProductoResponse]:
        return [ProductoMapper.to_response(obj) for obj in orm_list]
 
 
producto_mapper = ProductoMapper()
 
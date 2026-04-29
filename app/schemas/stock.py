
from pydantic import BaseModel, ConfigDict, field_validator


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StockResponse(SchemaBase):
    id:              int
    id_producto:     int
    cantidad_actual: int
    stock_minimo:    int
    bajo_minimo:     bool = False


class StockUpdate(BaseModel):
    stock_minimo: int

    @field_validator("stock_minimo")
    @classmethod
    def minimo_no_negativo(cls, v: int) -> int:
        if v < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
        return v
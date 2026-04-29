from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.orm import Session
from app.config.database import Base
 
ModelType  = TypeVar("ModelType",  bound=Base)
CreateType = TypeVar("CreateType")
UpdateType = TypeVar("UpdateType")
 
 
class BaseRepository(Generic[ModelType, CreateType, UpdateType]):
 
    def __init__(self, model: Type[ModelType]):
        self.model = model
 
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
 
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()
 
    def create(self, db: Session, schema: CreateType) -> ModelType:
        """
        model_dump() convierte el schema Pydantic a dict.
        **dict desempaqueta los campos como kwargs al constructor del modelo.
        """
        data = schema.model_dump()
        db_obj = self.model(**data)
        db.add(db_obj)
        db.flush()   # flush ≠ commit: manda el SQL pero no cierra la transacción.
                     # Permite obtener el id generado antes del commit final.
        db.refresh(db_obj)
        return db_obj
 
    def update(self, db: Session, db_obj: ModelType, schema: UpdateType) -> ModelType:
        """
        exclude_unset=True es clave: solo actualiza los campos que el cliente
        mandó explícitamente. Si mandó solo el precio, nombre no se toca.
        """
        data = schema.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.flush()
        db.refresh(db_obj)
        return db_obj
 
    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.flush()
        return db_obj
 
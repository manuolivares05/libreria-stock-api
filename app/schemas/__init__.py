from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
 
 
class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
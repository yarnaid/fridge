from pydantic import BaseModel, Field
import typing
from enum import Enum
from datetime import datetime
from datetime import timedelta


class Unit(str, Enum):
    kg = "kg"
    l = "l"
    g = "g"
    package = "package"


class Item(BaseModel):
    class Config:
        description = "Base entity stored in the fridge"
        schema_extra = {"example": {"name": "egg", "serving": 2.2, "unit": Unit.g}}

    id: typing.Optional[int] = Field(None, example=1234)
    name: str = Field(max_length=200, example="egg")
    serving: float = Field(..., gt=0)
    unit: Unit = Field(..., example=Unit.kg)
    stored_at: typing.Optional[datetime] = Field(default=datetime.now(), example=datetime(2020, 1, 1))
    outdated_at: typing.Optional[datetime] = Field(
        default=datetime.now() + timedelta(days=7), example=datetime(2020, 1, 1)
    )
    updated_at: typing.Optional[datetime] = Field(default=None, example=datetime(2020, 6, 1))

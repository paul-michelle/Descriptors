from framework.db.models import BaseModel
from framework.db.fields import Field


class SoftDrink(BaseModel):
    trademark = Field(max_length=16)
    producer = Field(max_length=16)

from pydantic import BaseModel,Field
from datetime import date as dt_date
from typing import Optional

class MorningMilkRecordSchema (BaseModel):
    cow_tag : str

    date : dt_date | None = None

    morning_milk : float 

class EveningMilkRecordSchema (BaseModel):
    cow_tag : str

    date : dt_date | None = None

    evening_milk : float = Field(ge=0)

class ResponseMilkRecord (BaseModel):
    id : int 

    date : dt_date | None = None

    morning_milk : Optional[float] = None

    evening_milk : Optional[float] = None

    milk_perDay : Optional[float] = None
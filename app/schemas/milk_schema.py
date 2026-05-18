from pydantic import BaseModel
from datetime import date as dt_date

class MorningMilkRecordSchema (BaseModel):
    cow_tag : str

    date : dt_date | None = None

    morning_milk : float 

class EveningMilkRecordSchema (BaseModel):
    cow_tag : str

    date : dt_date | None = None

    evening_milk : float 

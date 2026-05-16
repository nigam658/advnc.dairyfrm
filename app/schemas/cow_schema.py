from pydantic import BaseModel
from datetime import date as dt_date

class cowDataReq(BaseModel):

    cow_tag : str 
    breed : str
    age : float
    milk_per_day : float


class Cow_updateSchema(BaseModel):
    cow_tag : str
    breed :str
    age : float
    milk_per_day :  float
    

class get_single_cow_respons(BaseModel):
    cow_id : int
    cow_tag : str
    breed : str
    age : float
    milk_per_day : float

    model_config = {
        "from_attributes": True
    }

class MorningMilkRecordSchema (BaseModel):
    cow_tag : str

    date : dt_date | None = None

    morning_milk : float 

class EveningMilkRecordSchema (BaseModel):
    cow_tag : str

    date : dt_date | None = None

    evening_milk : float 

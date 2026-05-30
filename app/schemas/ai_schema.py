from pydantic import BaseModel,Field

class Chat_Request(BaseModel):
    message : str = Field (min_length = 2, max_length = 500)

class MonthlyMilkRequest(BaseModel):

    month: int = Field(ge=1, le=12)

    year: int = Field(ge=2000, le=2100)


class dailyTotalMilkRecord(BaseModel):
    month: int = Field(ge=1, le=12)

    year: int = Field(ge=2000, le=2100)

    day: int = Field(ge=1, le=31)



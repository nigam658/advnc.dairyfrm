from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from app.database import Base

class Cow(Base):
    __tablename__ = "cows"

    cow_id = Column(Integer, primary_key = True)
    cow_tag = Column(String(100), unique = True)
    breed = Column(String(100))
    age = Column(Float)
    milk_per_day = Column(Float)


# milk record table
class MilkRecord(Base):

    __tablename__ = "milk_records"

    id = Column(Integer, primary_key=True)

    cow_tag = Column(String(50),ForeignKey("cows.cow_tag"))

    date = Column(Date)

    morning_milk = Column(Float)

    evening_milk = Column(Float)

    milk_perDay = Column(Float)
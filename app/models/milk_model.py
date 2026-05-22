from app.database import Base
from sqlalchemy import Column, Integer, String,Float, ForeignKey, Date

# milk record table
class MilkRecord(Base):

    __tablename__ = "milk_records"

    id = Column(Integer, primary_key=True)

    cow_tag = Column(String(50),ForeignKey("cows.cow_tag"))

    date = Column(Date)

    morning_milk = Column(Float)

    evening_milk = Column(Float)

    milk_perDay = Column(Float)
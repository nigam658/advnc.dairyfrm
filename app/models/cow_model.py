from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from app.databases.mysqldb import Base

class Cow(Base):
    __tablename__ = "cows"

    cow_id = Column(Integer, primary_key = True)
    cow_tag = Column(String(100), unique = True)
    breed = Column(String(100))
    age = Column(Float)
    milk_per_day = Column(Float)


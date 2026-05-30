from app.databases.mysqldb import Base
from sqlalchemy import Column, String, Integer, Float

class SignpUser(Base):
    __tablename__ = "user_idpass"

    user_id = Column(Integer, primary_key=True)

    email = Column(String(100), unique=True)

    username = Column(String(100))

    password = Column(String(200))

    role = Column(String(50))



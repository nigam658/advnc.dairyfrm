from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# Engine , it create connection blueprint
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Parent class for all tables
Base = declarative_base()
 

def get_db ():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


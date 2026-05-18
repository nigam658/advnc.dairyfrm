from fastapi import FastAPI
from app.routers import auth, cow, milk
from app.models import cow_model, user_model
from app.database import Base, engine

app = FastAPI()

app.include_router(cow.router)
app.include_router(auth.router)
app.include_router(milk.router)

Base.metadata.create_all(bind=engine)
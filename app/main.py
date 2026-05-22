from fastapi import FastAPI
from app.routers import auth, cow, milk,ai_router
from app.models import cow_model, user_model
from app.database import Base, engine

app = FastAPI()

app.include_router(cow.router)
app.include_router(auth.router)
app.include_router(milk.router)
app.include_router(ai_router.router)

Base.metadata.create_all(bind=engine)
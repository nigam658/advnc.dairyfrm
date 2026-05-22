from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ai_schema import Chat_Request
from app.ai.chat_service import generate_response
from app.database import get_db

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("/chat")
def chat(data :Chat_Request,db : Session = Depends(get_db) ):
    
    output = generate_response(data.message, db)

    return {
        "response" : output
    }
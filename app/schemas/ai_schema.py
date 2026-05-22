from pydantic import BaseModel

class Chat_Request(BaseModel):
    message : str
from pydantic import BaseModel

class user_pass(BaseModel):

    email : str

    username :  str

    password : str


class LoginUser(BaseModel):
    username : str
    
    password : str
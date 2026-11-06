from pydantic import BaseModel

class Register(BaseModel):
    name:str
    username:str
    email:str
    password:str
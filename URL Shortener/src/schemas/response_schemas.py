from pydantic import BaseModel , EmailStr

class Register(BaseModel):
    name:str
    username:str
    email:EmailStr
    password:str

class Login(BaseModel):
    username_or_email:str
    password:str
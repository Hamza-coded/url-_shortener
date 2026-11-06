from src.utils.tokens_generation import access_token ,refresh_token, verify_access_token
from src.utils.Responses import AppError , AppResponse
from src.config.setting import settings
from ..models.users_models import User
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
import secrets 
from .mail_service import send_email
pass_hash = PasswordHash.recommended()

async def register_service(name,username,email,password,db:AsyncSession):
    hashed_pass = pass_hash.hash(password=password)
    user = User(
        name = name,
        username= username,
        email= email,
        password = hashed_pass
    )
    otp = secrets.SystemRandom().randint(100000,999999)
    db.add(user)
    db.commit
    await send_email(email,otp)
    

    
    
    




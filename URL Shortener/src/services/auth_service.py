from src.utils.Responses import AppError
from ..models.users_models import User
from ..models.otps_model import OTP
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
import secrets 
from .mail_service import send_email
from sqlalchemy import select , update , or_ , delete
import hashlib
from datetime import datetime , timezone , timedelta
from ..models.sessions_model import Session
from ..utils.tokens_generation import generate_access_token , generate_refresh_token , verify_access_token,verify_refresh_token


pass_hash = PasswordHash.recommended()


async def register_service(name,username,email,password,db:AsyncSession):
    otp = secrets.SystemRandom().randint(100000,999999)
    otpstr = (str(otp)).encode()
    otphash = hashlib.sha256(otpstr).hexdigest()
    exist = (await db.execute(select(User).where(
        or_(
            User.email == email,
            User.username == username
        )
        ))).scalar_one_or_none()
    if exist:
        if exist.is_verified == True:
            raise AppError(409,"User is already registered")
        else:
           await  db.execute(update(OTP).where(OTP.user_id == exist.id).values(otp = otphash , expires_at = datetime.now(timezone.utc)+ timedelta(minutes=5)))
           await db.commit()
    else:        
        hashed_pass = pass_hash.hash(password=password)
        user = User(
            name = name,
            username= username,
            email= email,
            password = hashed_pass
        )
        
        db.add(user)
        await db.commit()

        expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
        otp_db = OTP(
            user_id = user.id,
            otp = otphash,
            expires_at = expiry
        )
        
        db.add(otp_db)
        await db.commit()

    await send_email(email,otp)

async def otp_verification_service(user_id,otp:str,db:AsyncSession):
    otphash = hashlib.sha256(otp.encode()).hexdigest()
    otp_result = (await db.execute(select(OTP).where(OTP.user_id == user_id,OTP.otp == otphash ))).scalar_one_or_none()
    
    if not otp_result:
        raise AppError(401,"Invalid otp")

    if datetime.now(timezone.utc) > otp_result.expires_at:
        await db.delete(otp_result)
        await db.commit()
        raise AppError(401,"Invalid otp")

    
    user = await db.get(User,user_id)
    if not user:
         raise AppError(404,"user does not exist")

    user.is_verified = True
    await db.commit()

    await db.delete(otp_result)
    await db.commit()

    async with db.begin():
        session = Session(
            user_id = user_id,
            refresh_token_hash = "dummy",
            is_revoked = False
        )
        db.add(session)
        await db.flush()
        session_id = session.id 
        refresh_token = generate_refresh_token(user_id=user_id,session_id=session_id)
        session.refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    access_token = generate_access_token(user_id=user_id)
    return [refresh_token,access_token]
        
async def token_rotation_service(refresh_token,db:AsyncSession):
    if not refresh_token:
        raise AppError(401,"no refresh token")

    print("PAYLOAD TAK AAYA")
    payload = verify_refresh_token(refresh_token)
    if not payload:
        return False

    print("PAYLOAD TAK BAAHIR")
    refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    session_id = payload["session_id"] 
    user_id = payload["user_id"]
    session = (await db.execute(select(Session).where(
        Session.id == session_id, Session.user_id == user_id , Session.refresh_token_hash == refresh_token_hash
    ))).scalar_one_or_none()
    
    print("SESSION TAK AAYA")
    if not session :
        return False

    new_refresh_token = generate_refresh_token(user_id=user_id,session_id=session_id)
    new_access_token = generate_access_token(user_id=user_id)

    session.refresh_token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
    await db.commit()

    return [new_refresh_token,new_access_token]
    
async def login_service(username_or_email,password,db:AsyncSession):
    user = (await db.execute(select(User).where(
        or_(
           User.email == username_or_email,
           User.username == username_or_email
        ), User.is_verified == True
    ))).scalar_one_or_none()

    if not user: 
        raise AppError(404,"invalid details")

    pass_check = pass_hash.verify(password,user.password)


    if not pass_check :
        raise AppError(401,"invalid details")
    await db.commit()
    async with db.begin():
        session = Session(
        user_id = user.id,
        refresh_token_hash = "dummy",
        is_revoked = False
            )
        db.add(session)
        await db.flush()
        session_id = session.id 
        refresh_token = generate_refresh_token(user_id=user.id,session_id=session_id)
        session.refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    access_token = generate_access_token(user_id=user.id)
    return [refresh_token,access_token]

async def logout_service (refresh_token,db:AsyncSession):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        return 
    session_id = payload["session_id"]
    session = await db.get(Session,session_id)
    if not session:
        return 
    await db.delete(session)
    await db.commit()
    
async def logout_all_service(access_token,db:AsyncSession):
    payload = verify_access_token(access_token)
    user_id = payload["user_id"]
    await db.execute(delete(Session).where(Session.user_id==user_id))
    await db.commit()



    


    
    
    




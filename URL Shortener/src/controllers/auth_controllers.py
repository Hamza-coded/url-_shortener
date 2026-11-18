from ..utils.Responses import AppResponse ,AppError
from ..services.auth_service import register_service,otp_verification_service , token_rotation_service , login_service , logout_service
from fastapi.requests import Request
from fastapi.responses import Response


async def register_controller(user,db):
    await register_service(name=user.name,username=user.username,email=user.email,password=user.password,db=db)
    return AppResponse(success=True,message="User created successfully")

async def otp_verification_controller(user_id:int , otp:str , db, response):

    result = await otp_verification_service(user_id=user_id,otp=otp,db=db)
    refresh_token , access_token = result
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=30*24*60*60
    )
    return AppResponse(
        success=True,
        message="user verified successfully",
        data=access_token
    )

async def token_rotation_controller(db,request:Request,response:Response):
    refresh_token = request.cookies.get("refresh_token")
    result = await token_rotation_service(db=db,refresh_token=refresh_token)

    if not result :
        response.delete_cookie(key="refresh_token")
        raise AppError(status_code=401,message="invalid token")

    refresh_token , access_token = result
    response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            max_age=30*24*60*60)

    return AppResponse(
        success=True,
        message="token rotated successfully",
        data = access_token
    )
    
async def login_controller (user,db,response:Response):
    result = await login_service(user.username_or_email,user.password,db)
    refresh_token , access_token = result
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
       max_age=30*24*60*60)

    return AppResponse(
        success=True,
        message="logged-in successfully",
        data = access_token
    )

async def logout_controller(request:Request,response:Response,db):
    refresh_token = request.cookies.get("refresh_token")
    await logout_service(refresh_token=refresh_token,db=db)
    response.delete_cookie("refresh_token",
                           httponly=True,
                           secure=True,
                           path="/"
    )
    return AppResponse(
            success=True,
            message="logged-out successfully",
            data=None
        )

from fastapi import APIRouter , Response , Depends , Request
from ..utils.Responses import AppResponse
from ..controllers.auth_controllers import register_controller , otp_verification_controller , token_rotation_controller , login_controller , logout_controller
from ..schemas.response_schemas import Register , Login
from ..config.db import get_db
from ..utils.limiter import limiter

auth_router = APIRouter(
    prefix= "/api/auth",

)

@auth_router.post("/register",status_code=201,response_model=AppResponse)
async def register(user:Register,db = Depends(get_db)):
    return await register_controller(user,db)

@auth_router.post("/otp-verification/{user_id}/{otp}",status_code=200,response_model=AppResponse)
async def login(user_id:int,otp:str,response:Response,db=Depends(get_db)):
    return await otp_verification_controller(user_id,otp,db,response)

@auth_router.get("/refresh",status_code=200,response_model=AppResponse)
@limiter.limit("5/minute")
async def refresh(response:Response,request:Request,db=Depends(get_db)):
    return await token_rotation_controller(db=db,request=request,response=response)

@auth_router.post("/login",status_code=200,response_model=AppResponse)
@limiter.limit("5/minute")
async def login(user: Login, response:Response,request:Request,db=Depends(get_db)):
    return await login_controller(user=user,db=db,response=response)

@auth_router.get("/logout",status_code=200,response_model=AppResponse)
@limiter.limit("5/minute")
async def login(response:Response,request:Request,db=Depends(get_db)):
    return await logout_controller(request=request,response=response,db=db)
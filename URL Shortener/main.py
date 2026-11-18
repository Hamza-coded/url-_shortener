from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback
from src.utils.Responses import AppError
from src.routers.auth_router import auth_router
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from src.utils.limiter import limiter




app = FastAPI()

app.state.limiter = limiter
@app.exception_handler(Exception)
def exceptionHandler (req : Request , err : Exception):
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content= {
            "status": False,
            "message" : "Internal server error"
        } )


@app.exception_handler(RequestValidationError)
def validation_error (req : Request , err : RequestValidationError):
    print(traceback.format_exc())
    return JSONResponse(
        status_code=422,
        content= {
            "status": False,
            "message" : "Invalid Fields"
        } )

@app.exception_handler(AppError)
def app_error (req : Request , err : AppError):
    # print(traceback.format_exc())
    return JSONResponse(
        status_code= err.status_code,
        content= {
            "status": False,
            "message":err.message
        } )


# @app.post("/test",response_model=AppResponse,status_code=201)
# async def register (req:Register,db:AsyncSession=Depends(get_db)):
#     await register_service(req.name,req.username,req.email,req.password,db)
#     return AppResponse(success=True,message="user_created",data=None)

app.include_router(auth_router)
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
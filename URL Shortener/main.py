from fastapi import FastAPI , Request , Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback
from src.utils.Responses import AppError , AppResponse
from src.schemas.response_schemas import Register
from src.services.auth_service import register_service
from src.config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
app = FastAPI()

@app.exception_handler(Exception)
def exceptionHandler (req : Request , err : Exception):
    print(traceback.format_exc())
    return JSONResponse(
        status_code=400,
        content= {
            "status": False
        } )


@app.exception_handler(RequestValidationError)
def validation_error (req : Request , err : RequestValidationError):
    print(traceback.format_exc())
    return JSONResponse(
        status_code=422,
        content= {
            "status": False
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




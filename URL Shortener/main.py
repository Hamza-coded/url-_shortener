from fastapi import FastAPI , Request 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback
from src.utils.Responses import AppError , AppResponse

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


@app.get("/test",response_model=AppResponse,status_code=401,)
def test ():
    return AppResponse()
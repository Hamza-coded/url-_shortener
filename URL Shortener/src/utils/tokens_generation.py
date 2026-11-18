import jwt
from src.config.setting import settings
from datetime import  datetime , timedelta , timezone
from ..utils.Responses import AppError

def generate_refresh_token(user_id,session_id):
    payload = {"user_id":user_id, "session_id": session_id, "exp": datetime.now(timezone.utc)+timedelta(days=30)}
    return jwt.encode(payload,settings.REFRESH_TOKEN_KEY,algorithm="HS256")


def generate_access_token(user_id):
    payload = {"user_id":user_id, "exp": datetime.now(timezone.utc)+timedelta(minutes=15)}
    return jwt.encode(payload,settings.ACCESS_TOKEN_KEY,algorithm="HS256")


def verify_access_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_TOKEN_KEY,
            algorithms="HS256"
        )
        return payload
    except Exception as e:
        return False

def verify_refresh_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_TOKEN_KEY,
            algorithms="HS256"
        )
        return payload
    except Exception as e:
           raise AppError(401,"Invalid credentials")
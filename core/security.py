import bcrypt
import os
import jwt
from datetime import datetime,timedelta
from jose import JWTError
from typing import Any
from itsdangerous import URLSafeTimedSerializer
from core.config import settings

def hash_password(password):
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

def verify_password(plain_password:str, hashed_password:str)->bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def generate_access_token(user_id:int):
    payload = {
        "sub":str(user_id),
        "role": user_id.role,
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }
    return jwt.encode(
        payload,
        os.getenv('JWT_ACCESS_SECRET'),
        algorithm='HS256'
    )

def generate_refresh_token(user_id:int):
    payload={
        "sub":str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    return jwt.encode(
        payload,
        os.getenv('JWT_REFRESH_SECRET'),
        algorithm='HS256'
    )

def decode_token(token:str,secret:str)->dict[str,Any]:
    return jwt.decode(
        token,
        secret,
        algorithms=['HS256']
    )
_email_serializer = URLSafeTimedSerializer(
    settings.JWT_EMAIL_SECRET,salt="email-verify")

_reset_serializer=URLSafeTimedSerializer(
    settings.JWT_PASSWORD_SECRET,salt="pw-reset"
)

def create_email_verification_token(email:str)->str:
    return _email_serializer.dumps(email)

def email_verify_token(token:str)->str|None:
    try:
        max_age=settings.EMAIL_VERIFICATION_EXPIRE_HOURS*3600
        return _email_serializer.loads(token,max_age=max_age)
    except Exception:
        return None
    
def create_password_reset_token(email:str)->str:
    _reset_serializer.dumps(email)

def verify_password_reset_token(user_id:int):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(
        payload,
        os.getenv('JWT_PASSWORD_SECRET'),
        algorithm='HS256'
    )


        


   


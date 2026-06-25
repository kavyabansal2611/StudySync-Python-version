import bcrypt
import os
import jwt
from datetime import datetime,timedelta

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

def generate_access_token(user):
    payload = {
        "id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }
    return jwt.encode(
        payload,
        os.getenv('JWT_ACCESS_SECRET'),
        algorithm='HS256'
    )

def generate_refresh_token(user):
    payload={
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    return jwt.encode(
        payload,
        os.getenv('JWT_REFRESH_SECRET'),
        algorithm='HS256'
    )

def email_Verify_token(user):
    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(
        payload,
        os.getenv('JWT_EMAIL_SECRET'),
        algorithm='HS256'
    )

def password_reset_token(user):
    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    return jwt.encode(
        payload,
        os.getenv('JWT_PASSWORD_SECRET'),
        algorithm='HS256'
    )



from datetime import datetime
from pydantic import BaseModel,EmailStr,Field,ConfigDict,field_validator
import re
from typing import Literal
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str
    email:EmailStr
    username:str
    password_hash:str
    year_of_study:int
    is_verified:bool
    created_at:datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password:str
    year_of_study:int
    username:str
    @field_validator("password")
    @classmethod
    def password_strength(cls,v:str)->str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    username: str
    email: EmailStr
    year_of_study: int
    created_at: datetime
    is_verified: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    is_verified: bool

class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str="bearer"

class RefreshRequest(BaseModel):
    refresh_token:str

class PasswordResetRequest(BaseModel):
    email:EmailStr

class PasswordResetConfirm(BaseModel):
    token:str
    new_password:str
    @field_validator("new_password")
    @classmethod
    def password_strength(cls,v:str)->str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class MessageResponse(BaseModel):
    message:str

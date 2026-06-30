from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
from fastapi import HTTPException,status
from models.Usermodel import User
from schemas.User_schema import (UserLogin,UserCreate,PasswordResetConfirm,PasswordResetRequest)
from services.email_service import send_verification_email
from core.security import (hash_password,verify_password,decode_token,generate_access_token,generate_refresh_token,email_verify_token,verify_password_reset_token,create_password_reset_token,create_email_verification_token)
from services.email_service import (send_verification_email,password_reset_mail)
import jwt


async def register(user:UserCreate,db:AsyncSession):
    try:
        result= await db.execute(select(User).where(User.email==user.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400,detail="User already exists. Please login")
        new_user=User(
            name=user.name,
            username=user.username,
            email=user.email,
            year_of_study=user.year_of_study,
            password_hash=hash_password(user.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        email_sent = True
        try:
            token = create_email_verification_token(user.email)
            await asyncio.to_thread(send_verification_email, user.email, token)
        except Exception:
            email_sent = False

        return{
            "user":new_user.to_safe_dict(),
            "email_sent":email_sent
        }
    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500,detail="Internal server error")

async def login(user:UserLogin,db:AsyncSession):
    try:
       result=await db.execute(select(User).where(User.email==user.email))
       existing_user=result.scalar_one_or_none()
       if not existing_user or not verify_password(user.password,existing_user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid credentials")
       if not existing_user.is_active():
        raise HTTPException(status_code=400,detail="Account disabled")
       refresh_token=generate_refresh_token(str(existing_user.id))
       existing_user.refresh_token=refresh_token
       await db.commit()

       return{
           "access token":generate_access_token(existing_user.id),
           "refresh_token":refresh_token,
           "user":existing_user.to_safe_dict()
       }
    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500,detail="Internal server error")

async def refresh_tokens(refresh_token:str,db:AsyncSession)->dict:
    try:
        payload=decode_token(refresh_token)
        if payload.get("type")!="refresh":
            raise HTTPException(status_code=401,detail="Invalid credentials")
        user_id=payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401,detail="Invalid or expired")
    try:
        result= await db.execute(select(User).where(User.id==user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401,detail="Invalid token")
        if user.refresh_token!=refresh_token:
            user.refresh_token = None
            await db.commit()
            raise HTTPException(status_code=401,detail="Please login again")
        new_access_token=generate_access_token(user_id)
        new_refresh_token=generate_refresh_token(user_id)
        user.refresh_token=new_refresh_token
        await db.commit()
        return{
            "access_token":new_access_token,
            "refresh_token":new_refresh_token
        }
    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
       
 
async def send_verification(email:str,db:AsyncSession):
    result=await db.execute(select(User).where(User.email==email))
    user=result.scalar_one_or_none()
    if user and not user.is_verified:
        token=create_email_verification_token(email)
        await asyncio.to_thread(send_verification_email, user.email, token)  

async def verify_email(token:str,db:AsyncSession):
    try:
        email=email_verify_token(token)
        if not email:
            raise HTTPException(status_code=400,detail="Invalid token")
        result = await db.execute(select(User).where(User.email==email))
        user=result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401,detail="Invalid credentials")
        if user.is_verified:
            return
        user.is_verified = True
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500,detail="Internal Server Error")
    
async def request_password_reset(payload:PasswordResetRequest,db:AsyncSession):
    result= await db.execute(select(User).where(User.email==payload.email))
    user=result.scalar_one_or_none()
    if user:
        token= create_password_reset_token(payload.email)
        await asyncio.to_thread(password_reset_mail, payload.email, token)

async def reset_password(user:PasswordResetConfirm,db:AsyncSession):
    email=verify_password_reset_token(user.token)
    if not email:
        raise HTTPException(status_code=400,detail="Invalid token")
    result=await db.execute(select(User).where(User.email==email))
    existing_user=result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    existing_user.password_hash=hash_password(user.new_password)
    await db.commit()



    





    
    
    

    





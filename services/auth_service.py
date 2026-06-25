from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import Depends,HTTPException
import model
import schemas
from services.email_service import send_verification_email
from core.security import hash_password,verify_password,generate_access_token,generate_refresh_token,email_Verify_token,password_reset_token

from database import get_db


async def register(user:schemas.User_schema.UserCreate,db:Session):
    try:
        existing_user=db.query(model.User).filter(or_(model.User.email==user.email,model.User.username==user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400,detail="User exists already")
        new_user=model.User(
            email=user.email,
            name=user.name,
            year_of_study=user.year_of_study,
            username=user.username,
            password_hash=hash_password(user.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token=generate_access_token(new_user.id)
        refresh_token=generate_refresh_token(new_user.id)
        
        new_user.refresh_token=refresh_token
        db.commit()

        email_token=email_Verify_token(new_user.id)
        try:
            await send_verification_email(new_user.email,email_token)
        except Exception as e:
            raise HTTPException(status_code=500,detail="Failed to send email verification")
        return {
            "user":new_user.to_safe_dict(),
            "access_token":access_token,
            "refresh_token": refresh_token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail="Internal Server error")

async def login(user:schemas.User_schema.UserLogin,db:Session):
    try:
        existing_user=db.query(model.User).filter(model.User.email==user.email).first()

        if not existing_user:
            raise HTTPException(status_code=401,detail="Invalid credentials")
        if not existing_user.is_verified:
            raise HTTPException(status_code=403,detail="Please verify your mail")
        if not  (verify_password(user.password,existing_user.password_hash)):
            raise HTTPException (status_code=401,detail="Invalid credentials")
        access_token=generate_access_token(existing_user.id)
        refresh_token=generate_refresh_token(existing_user.id)
        existing_user.refresh_token=refresh_token

        db.commit()
        return {
            "user":existing_user.to_safe_dict(),
            "access_token":access_token,
            
        }
    except HTTPException:
        raise
    except Exception :
        db.rollback()

        raise HTTPException(status_code=500,detail="Internal Server error")




    
    
    

    





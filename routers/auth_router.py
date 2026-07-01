from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_db,get_current_user
from services import auth_service
from schemas.User_schema import (UserCreate,UserLogin,TokenResponse,RefreshRequest,PasswordResetRequest,PasswordResetConfirm,MessageResponse)
from models.Usermodel import User

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=MessageResponse)
async def register(payload:UserCreate,db:AsyncSession=Depends(get_db)):
    await auth_service.register(payload,db)
    return{"message":"account successfully created"}

@router.post("/login",response_model=TokenResponse)
async def login(payload:UserLogin,db:AsyncSession=Depends(get_db)):
    return await auth_service.login(payload,db)
    
@router.post("/send-verification-email",response_model=MessageResponse)
async def send_verification_email(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await auth_service.send_verification(current_user.email, db)
    return {"message": "Verification email sent "}

@router.get("/verify-email", response_model=MessageResponse)
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    await auth_service.verify_email(token, db)
    return {"message": "Email verified successfully."}

@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(payload: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    await auth_service.request_password_reset(payload, db)
    return {"message": "a reset link has been sent to registered email."}


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(payload: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    await auth_service.reset_password(payload,db)
    return {"message": "Password reset successfully."}


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await auth_service.logout_user(current_user, db)
    return {"message": "Logged out"}
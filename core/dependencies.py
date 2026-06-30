from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from core.security import decode_token
from models.Usermodel import User
from sqlalchemy import select
from core.config import settings

bearer_scheme=HTTPBearer(auto_error=False)

async def get_current_user(
        credentials: HTTPAuthorizationCredentials=Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db)
        )->User:
            token=credentials.credentials
            credentials_exception=HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Credentials",
                    headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload=decode_token(token,settings.JWT_ACCESS_SECRET)
                if payload.get("type")!="access":
                        raise credentials_exception
                user_id:str=payload.get("sub")
                if not user_id:
                        raise credentials_exception
            except jwt.PyJWTError:
                    raise credentials_exception
            result = await db.execute(select(User).where(User.id == int(user_id)))
            user=result.scalar_one_or_none()
            if not user:
                    raise credentials_exception
            return user
async def get_verified_user(current_user:User=Depends(get_current_user))->User:
        if not current_user.is_verified:
                raise HTTPException(
                        status_code=403,
                        detail="Email not verified"
                )
        return current_user

    

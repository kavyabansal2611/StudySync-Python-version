from fastapi import FastAPI
import uvicorn
from routers.auth_router import router as auth_router
from core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(auth_router, prefix="/api/v1")



1   
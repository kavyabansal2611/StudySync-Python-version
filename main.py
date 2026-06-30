from fastapi import FastAPI,Depends,HTTPException
import uvicorn
from sqlalchemy.orm import Session
from database import get_db
import model,schemas
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine

model.Base.metadata.create_all(bind=engine)
app = FastAPI()






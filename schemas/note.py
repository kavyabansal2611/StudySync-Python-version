from datetime import datetime
from pydantic import BaseModel,ConfigDict


class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    title:str
    content:str
    created_at:datetime


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


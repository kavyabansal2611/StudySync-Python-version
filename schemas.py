from datetime import datetime
from pydantic import BaseModel,EmailStr,Field,ConfigDict,field_validator
import re
from typing import Literal

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Subject(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    subject_name:str
    classes_per_week:int

class Attendance(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    subject_id: int
    date: datetime
    present: bool

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    title:str
    description:str
    date:datetime
    deadline:datetime
    status:Literal["pending","completed","cancelled"]=Field(default="pending")
    priority:int=Field(...,ge=1,le=3)

class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    title:str
    description:str
    event_date:datetime

class Note(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    title:str
    content:str
    created_at:datetime

class SubjectCreate(BaseModel):
    subject_name:str
    classes_per_week: int

class AttendanceCreate(BaseModel):
    date:datetime
    present:bool

class SubjectUpdate(BaseModel):
    subject_name:str | None=None
    classes_per_week: int | None=None


class AttendanceUpdate(BaseModel):
    date:datetime | None = None
    present:bool | None=None


class TaskCreate(BaseModel):

    title:str
    description:str
    deadline:datetime
    status:Literal["pending","completed","cancelled"]=Field(default="pending")
    priority: int = Field(..., ge=1, le=3)

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None
    status: Literal["pending", "completed","cancelled"] | None = None
    priority: int | None=Field(default=None, ge=1, le=3)

class EventCreate(BaseModel):
    title:str
    description:str
    event_date:datetime

class EventUpdate(BaseModel):
    title:str | None = None
    description: str | None = None
    event_date:datetime | None = None

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


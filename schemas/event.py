from datetime import datetime
from pydantic import BaseModel,ConfigDict

class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    title:str
    description:str
    event_date:datetime


class EventCreate(BaseModel):
    title:str
    description:str
    event_date:datetime

class EventUpdate(BaseModel):
    title:str | None = None
    description: str | None = None
    event_date:datetime | None = None

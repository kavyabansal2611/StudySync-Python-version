from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from database import Base
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)
    title=Column(String,nullable=False)
    description=Column(Text,nullable=False)
    event_date=Column(DateTime,nullable=False)

    user = relationship("User", back_populates="events")
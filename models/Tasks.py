from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from database import Base
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)
    title=Column(String,nullable=False)
    description=Column(Text,nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    deadline=Column(DateTime,nullable=False)
    priority=Column(Integer,nullable=False)
    status=Column(String,nullable=False)

    user=relationship("User",back_populates="tasks")
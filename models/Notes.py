from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from database import Base
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)

    title=Column(String,nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)

    user = relationship("User", back_populates="notes")
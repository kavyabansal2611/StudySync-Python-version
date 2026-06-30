import email

from sqlalchemy import Column, Integer, String, DateTime,Boolean

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime,timezone
from database import Base

class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    username=Column(String,nullable=False,unique=True)
    email=Column(String,unique=True,nullable=False)
    password_hash=Column(String,nullable=False)
    year_of_study=Column(Integer,nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    is_verified=Column(Boolean,nullable=False,default=False)
    is_active=Column(Boolean,nullable=False,default=True)

    subjects = relationship("Subject", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    def to_safe_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "year_of_study":self.year_of_study,
            "is_verified": self.is_verified,

        }

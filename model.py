from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from database import Base

class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password_hash=Column(String,nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)

    subjects = relationship("Subject", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)
    subject_name=Column(String,nullable=False)
    classes_per_week = Column(Integer,nullable=False)

    attendance=relationship("Attendance", back_populates="subject", cascade="all, delete-orphan")
    user=relationship("User", back_populates="subjects")

class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer,primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False, index=True)
    present=Column(Boolean,nullable=False,default=False)
    date=Column(DateTime,nullable=False)

    subject=relationship("Subject",back_populates="attendance")

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

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)
    title=Column(String,nullable=False)
    description=Column(Text,nullable=False)
    event_date=Column(DateTime,nullable=False)

    user = relationship("User", back_populates="events")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)

    title=Column(String,nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)

    user = relationship("User", back_populates="notes")





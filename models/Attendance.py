from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer,primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False, index=True)
    present=Column(Boolean,nullable=False,default=False)
    date=Column(DateTime,nullable=False)

    subject=relationship("Subject",back_populates="attendance")

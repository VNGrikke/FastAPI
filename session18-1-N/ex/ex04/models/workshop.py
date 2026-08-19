from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from database.database import Base

class WorkshopStatus(str, enum.Enum):
    UPCOMING = "UPCOMING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class RegistrationStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"

class Workshop(Base):
    __tablename__ = "workshops"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    max_participants = Column(Integer, nullable=False)
    status = Column(SQLEnum(WorkshopStatus), default=WorkshopStatus.UPCOMING)
    start_time = Column(DateTime, nullable=False)

    registrations = relationship("Registration", back_populates="workshop")

class Registration(Base):
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(SQLEnum(RegistrationStatus), default=RegistrationStatus.REGISTERED)

    student = relationship("Student", back_populates="registrations")
    workshop = relationship("Workshop", back_populates="registrations")
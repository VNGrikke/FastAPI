from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    class_code = Column(String(50), unique=True, index=True)
    class_name = Column(String(100))
    max_students = Column(Integer)
    status = Column(String(20), default="active")
    
    students = relationship("Student", back_populates="classroom")
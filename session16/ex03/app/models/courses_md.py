from session16.ex03.app.database.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__  = "courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    max_students = Column(Integer, nullable=False)
    
    enrollments = relationship("Enrollment", back_populates="course")
    students = relationship("Student", secondary="enrollments", back_populates="courses")
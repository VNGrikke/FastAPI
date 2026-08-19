from ..database.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Liên kết với bảng Student
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student = relationship("Student", back_populates="enrollments")
    
    # Liên kết với bảng Course
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False) 
    course = relationship("Course", back_populates="enrollments") 

    enrolled_at = Column(DateTime, default= datetime.now())
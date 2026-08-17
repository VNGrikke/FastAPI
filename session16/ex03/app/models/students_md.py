from session16.ex03.app.database.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), default='ACTIVE')
    
    enrollments = relationship("Enrollment", back_populates="student")
    courses = relationship("Course", secondary="enrollments", back_populates="students")
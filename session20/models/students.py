from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    gender = Column(String(10))
    class_id = Column(Integer, ForeignKey("classrooms.id"))
    
    classroom = relationship("Classroom", back_populates="students")
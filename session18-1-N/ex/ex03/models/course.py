from ..database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

    # Khai báo mối quan hệ ngược lại với bảng Enrollment
    enrollments = relationship("Enrollment", back_populates="course")
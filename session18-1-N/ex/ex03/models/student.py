from ..database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False) # Nên cho độ dài chuỗi
    status = Column(String(20), nullable=False)

    # Khai báo mối quan hệ ngược lại với bảng Enrollment
    enrollments = relationship("Enrollment", back_populates="student")
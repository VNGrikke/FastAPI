from fastapi import FastAPI
from .database.database import Base,engine
from .routers.student import router_student
from .routers.course import router_course
from .routers.enrollment import router_enrollment
from .models.student import Student
from .models.course import Course
from .models.enrollment import Enrollment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_student)
app.include_router(router_course)
app.include_router(router_enrollment)

@app.get("/")
def test():
    return{"message": "server chay thanh cong"}

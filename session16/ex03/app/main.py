from fastapi import FastAPI
from session16.ex03.app.routers.student_rt import router_student
from session16.ex03.app.routers.enrollment_rt import router_enrollment

app = FastAPI()
app.include_router(router_student)
app.include_router(router_enrollment)

@app.get("/")
def home():
    return {
        "message":"API đang chạy!"
    }
from fastapi import FastAPI

app = FastAPI(
    title= "My API"
)

students = [
    {"id": 1, "name": "VUONG"},
    {"id": 2, "name": "VU"}
]

@app.get("/students")
def home():
    return {"id": 1, "name": "VUONG", "age": 21, "pass": True}


@app.get("/students/{student_id}", summary="Lay ra thong tin sinh vien")
def getStudent(student_id:int):
    for student in students:
        if student["id"] == student_id:
            return student
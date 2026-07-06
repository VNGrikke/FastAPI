from fastapi import FastAPI
app = FastAPI()


students = [
    {"id": 1, "name": "An", "status": "pending"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "pending"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students", summary= "danh sach hoc sinh")
def get_student():
    return students


@app.get("/students/active", summary= "danh sach hoc sinh active")
def get_student_active():
    student_active = []
    result = {
        "message" : "Danh sách sinh viên đang học",
        "data" : student_active
    }
    for student in students:
        if student["status"] == "active":
            student_active.append(student)
    if student_active == [] : 
        result["message"] == "Khong co hoc sinh theo hoc"
    return result



from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class StudentCreateRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Mã học viên không được để trống")
    name: str = Field(..., min_length=1, description="Tên không được để trống")
    email: EmailStr = Field(..., description="Email không đúng định dạng hoặc không được để trống")
    age: int = Field(..., gt=0, description="Tuổi phải lớn hơn 0")

class StudentUpdateRequest(BaseModel):
    code: str | None = Field(None, min_length=1)
    name: str | None = Field(None, min_length=1)
    email: EmailStr | None = Field(None)
    age: int | None = Field(None, gt=0)


def check_duplicate_student_code(code: str):
    for student in students:
        if student["code"] == code:
            return student
    return None

def find_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


@app.get("/students")
def get_students(keyword: str = None, min_age: int = 0, max_age: int = 0):
    filter_students = students

    if keyword is not None:
        kw = keyword.lower()
        filter_students = [
            student for student in filter_students 
            if kw in student["code"].lower() 
            or kw in student["name"].lower() 
            or kw in student["email"].lower()
        ]

    if min_age > 0:
        filter_students = [student for student in filter_students if student["age"] >= min_age]

    if max_age > 0:
        filter_students = [student for student in filter_students if student["age"] <= max_age]

    return {
        "message": "Lấy danh sách thành công" if len(filter_students) else "Không tìm thấy học viên nào",
        "data": filter_students 
    }

@app.post("/students")
def create_student(new_student: StudentCreateRequest):
    if check_duplicate_student_code(new_student.code):
        return {
            "message": "Code đã tồn tại"
        }
    
    student_dict = new_student.model_dump()
    new_id = max([s["id"] for s in students], default=0) + 1
    student_dict["id"] = new_id
    
    students.append(student_dict)

    return {
        "message": "Thêm mới học viên thành công",
        "data": student_dict
    }

@app.get("/students/{student_id}")
def detail_student(student_id: int):
    student = find_student_by_id(student_id)
    if student:
        return {
            "message": "Tìm thấy học viên",
            "data": student
        }

    return {
        "message": "Student not found",
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, update_data: StudentUpdateRequest):
    student = find_student_by_id(student_id)

    if not student:
        return {
            "message": "Student not found"
        }

    if update_data.code is not None and update_data.code != student["code"]:
        if check_duplicate_student_code(update_data.code):
            return {
                "message": "Code đã tồn tại ở học viên khác"
            }        
        student["code"] = update_data.code

    if update_data.name is not None:
        student["name"] = update_data.name

    if update_data.email is not None:
        student["email"] = update_data.email

    if update_data.age is not None:
        student["age"] = update_data.age

    return {
        "message": "Cập nhật thành công",
        "data": student
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student = find_student_by_id(student_id)
    if student:
        students.remove(student)
        return {
            "message": "Xóa thành công",
            "data": student
        }
    
    return {
        "message": "Student not found",
    }
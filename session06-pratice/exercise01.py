from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

app = FastAPI()

class CreateRequest(BaseModel):
    code: str = Field(..., description= "khong duoc de trong")
    name: str = Field(..., description= "khong duoc de trong")
    duration: int = Field(..., gt = 0, description= "phai lon hon 0")
    fee: float = Field(..., ge = 0, description= "phai lon hon hoac bang 0")

class UpdateRequest(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0, description="phai lon hon 0")
    fee: Optional[float] = Field(None, ge=0, description="phai lon hoac bang 0")


@app.get("/courses")
def get_courses(keywords:str = None, min_fee:int = 0, max_fee:int = 0):
    filter_course = courses

    if keywords is not None:
        filter_course = [course for course in courses if keywords.lower() in course["code"] or keywords.lower() in course["name"]]

    if min_fee > 0:
        filter_course = [course for course in courses if min_fee < course["fee"]]

    if max_fee > 0:
        filter_course = [course for course in courses if max_fee > course["fee"]]

    return {
        "message": "Lấy danh sách thành công" if len(filter_course) else "Lấy danh sách không thành công",
        "data": filter_course 
    }
    
def check_duplicate_code(code):
    for course in courses:
        if course["code"] == code:
            return course

    return None

def find_by_id(id):
    for course in courses:
        if course["id"] == id:
            return course

    return None

@app.post("/courses")
def create_course(new_course: CreateRequest):
    if check_duplicate_code(new_course.code):
        return {
            "message" : "code da ton tai"
        }
    course_dict = new_course.model_dump()
    
    new_id = max([c["id"] for c in courses], default=0) + 1
    course_dict["id"] = new_id
    
    courses.append(course_dict)

    return {
        "message" : "Them moi khoa hoc thanh cong",
        "data" : course_dict
    }


@app.get("/course/{course_id}")
def detail_course(course_id: int):
    course = find_by_id(course_id)
    if course:
        return {
            "message" : "Tim thay khoa hoc",
            "data" : course
        }

    return {
            "message" : "Khoa hoc khong ton tai",
    }

@app.put("/course/{course_id}")
def update_course(course_id: int, update_course: UpdateRequest):
    course = find_by_id(course_id)

    if not course:
        return {
            "message" : "Khoa hoc khong ton tai"
        }
    

    if update_course.code is not None and update_course.code != course["code"]:
            if check_duplicate_code(update_course.code):
                return{
                    "message" : "Code da ton tai"
                }        
            course["code"] = update_course.code

    if update_course.name is not None:
        course["name"] = update_course.name

    if update_course.duration is not None:
        course["duration"] = update_course.duration

    if update_course.fee is not None:
        course["fee"] = update_course.fee

    return {
        "message" : "Cap nhat thanh cong",
        "data" : course
    }


@app.delete("/course/{course_id}")
def delete_course(course_id:int):
    course = find_by_id(course_id)
    if course:
        courses.remove(course)
        return {
            "message" : "Xoa thanh cong",
            "data" : course
        }
    
    return {
        "message" : "Xoa khong thanh cong",
    }
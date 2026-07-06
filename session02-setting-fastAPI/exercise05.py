from fastapi import FastAPI

app = FastAPI()

students = [
    {
        "id": 1,
        "name": "Nguyen Van Vuong",
        "status": "Đang học"
    },
    {
        "id": 2,
        "name": "Le Thi Mai",
        "status": "Đang học"
    }
]


# 1. Xem danh sách sinh viên
@app.get("/students", summary="Danh sách sinh viên")
def get_students():
    return {
        "message": "Danh sách sinh viên",
        "data": students
    }


# 2. Xem chi tiết sinh viên
@app.get("/students/detail", summary="Chi tiết sinh viên")
def get_student_detail():
    if len(students) == 0:
        return {
            "message": "Danh sách sinh viên trống",
            "data": {}
        }

    return {
        "message": "Chi tiết sinh viên đầu tiên",
        "data": students[0]
    }


# 3. Thêm sinh viên
@app.post("/students", summary="Thêm sinh viên")
def add_student():
    new_student = {
        "id": len(students) + 1,
        "name": "Sinh Vien Moi",
        "status": "Đang học"
    }

    students.append(new_student)

    return {
        "message": "Thêm sinh viên thành công",
        "data": new_student
    }


# 4. Cập nhật sinh viên
@app.put("/students", summary="Cập nhật sinh viên")
def update_student():
    if len(students) == 0:
        return {
            "message": "Không có sinh viên để cập nhật",
            "data": {}
        }

    students[0]["name"] = "Nguyen Van A (Đã cập nhật)"
    students[0]["status"] = "Đã tốt nghiệp"

    return {
        "message": "Cập nhật thành công",
        "data": students[0]
    }


# 5. Xóa sinh viên
@app.delete("/students", summary="Xóa sinh viên")
def delete_student():
    if len(students) == 0:
        return {
            "message": "Không có sinh viên để xóa",
            "data": []
        }

    deleted_student = students.pop()

    return {
        "message": "Xóa sinh viên thành công",
        "data": deleted_student
    }


# 6. Thống kê
@app.get("/students/statistic", summary="Thống kê sinh viên")
def statistic_student():
    studying = 0
    graduated = 0

    for student in students:
        if student["status"] == "Đang học":
            studying += 1
        else:
            graduated += 1

    return {
        "message": "Thống kê sinh viên",
        "data": {
            "tong_sinh_vien": len(students),
            "dang_hoc": studying,
            "da_tot_nghiep": graduated
        }
    }
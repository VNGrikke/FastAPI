# Endpoint hiện tại: /student
# Lỗi 404: Do gọi /students nhưng code chỉ định nghĩa /student.
# Tên sai chuẩn: Dùng số ít (/student) cho danh sách là sai, phải dùng số nhiều.
# Sai logic: students[0] chỉ lấy phần tử đầu tiên (1 sinh viên), không lấy cả danh sách.
# Đường dẫn chuẩn: /students

from fastapi import FastAPI
app = FastAPI()


students = [
    {"id": 1, "name": "VUONG"},
    {"id": 2, "name": "VU"},
    {"id": 2, "name": "NAM"}
]

@app.get("/students", summary= "danh sach hoc sinh")
def get_student():
    return students




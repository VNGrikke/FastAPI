# 1. Lỗi hiện tại
# Dữ liệu: Dùng str() và cộng chuỗi khiến API trả về một đoạn text duy nhất thay vì mảng JSON, làm Frontend không thể đọc được.
# Tên endpoint: Dùng động từ /getStudents là sai chuẩn RESTful (chỉ nên dùng danh từ).

# 2. Cách sửa
# Đổi endpoint thành /students.
# Trả về trực tiếp biến list students để FastAPI tự động tạo JSON array.


from fastapi import FastAPI
app = FastAPI()
students = ["Vuong", "Nam", "Vu"]

@app.get("/students", summary= "danh sach hoc sinh")
def get_student():
    return students
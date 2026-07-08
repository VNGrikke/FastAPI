# Phần 1: Phân tích & Đề xuất giải pháp
# 1. Phân tích Input / Output
# Input: Request body định dạng JSON chứa: full_name, email (bắt buộc) và age, course, phone (tùy chọn).

# Output:

# Thành công: HTTP 201/200 kèm dữ liệu học viên vừa tạo.

# Thất bại: HTTP 422 (lỗi thiếu/sai định dạng dữ liệu - Bẫy 1 & 2) hoặc HTTP 400 (lỗi email trùng lặp - Bẫy 3).

# 2. Hai giải pháp đề xuất
# Giải pháp 1 (Xác thực thủ công): Nhận request dưới dạng dict. Tự viết các khối lệnh if/else và dùng Regex để kiểm tra từng trường hợp (thiếu key, độ dài, định dạng email).

# Giải pháp 2 (Sử dụng Pydantic Model): Dùng công cụ tích hợp sẵn của FastAPI. Định nghĩa class kế thừa BaseModel, sử dụng type-hinting (EmailStr, Field) để framework tự động kiểm tra và báo lỗi.


# Phần 2: So sánh & Lựa chọn1. 
# Bảng so sánh     
# Tiêu chí                                  Giải pháp 1 (Xác thực thủ công)                 Giải pháp 2 (Dùng Pydantic)
# Độ dễ hiểuKém (nhiều if/else rối mắt).    Rất cao (đọc class là hiểu schema).             Code cần viếtNhiều (phải tự viết Regex, check rỗng).
# Rất ít (chỉ cần khai báo kiểu dữ liệu).   Kiểm soát lỗiTự quản lý code lỗi, dễ thiếu sót. Tự động trả về HTTP 422 chuẩn OpenAPI.
# Cấu trúc dữ liệu                          Không rõ ràng (dùng dict chung chung).          Cực kỳ rõ ràng (có type-hinting cho IDE).
# 
# 
# 2. Chốt lựa chọn giải pháp
# Lựa chọn: 
# Giải pháp 2 (Sử dụng Pydantic Model)Lý do: Đây là phương pháp tối ưu và chuẩn xác nhất khi làm việc với FastAPI. 
# Pydantic sẽ tự động bắt và xử lý gọn gàng Bẫy 1 & 2 (thiếu dữ liệu, sai format email) mà không cần code logic phức tạp. 
# Nhờ đó, file Controller sẽ rất "sạch" và chỉ cần tập trung xử lý duy nhất quy tắc nghiệp vụ là Bẫy 3 (kiểm tra trùng email).

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()

# Tạo hẳn 1 mảng (List) để lưu trữ dữ liệu
# Khởi tạo sẵn 1 record giả lập để test Bẫy 3
students_db = [
    {
        "full_name": "Người Cũ",
        "email": "existing@gmail.com",
        "age": 25,
        "course": "react",
        "phone": "0111222333"
    }
]

class StudentCreate(BaseModel):
    full_name: str = Field(..., min_length=3, strip_whitespace=True)
    email: EmailStr 
    age: Optional[int] = None
    course: Optional[str] = None
    phone: Optional[str] = None

@app.post("/students")
async def create_student(student: StudentCreate):
    for existing_student in students_db:
        if existing_student["email"] == student.email:
            return {
                "detail": "Email đã tồn tại trong hệ thống"
            }
    
    new_student = student.model_dump()
    
    # Thêm học viên mới vào mảng
    students_db.append(new_student)
    
    return {
        "message": "Thêm học viên thành công",
        "data": new_student
    }

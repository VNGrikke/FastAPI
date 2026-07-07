# 1. Phân tích Input/Output

# Input: Danh sách sách (có id, title, quantity).

# Output: JSON { "message": "...", "data": [...] }.

# Điều kiện: Sách có trường quantity, và 0 <= quantity <= 5.

# 2. Đề xuất giải pháp

# Giải pháp 1: Dùng vòng lặp for kết hợp câu lệnh if.

# Giải pháp 2: Dùng List comprehension.

# 3. Lựa chọn giải pháp

# Chọn Giải pháp 1 (Vòng lặp for).

# Lý do: Dễ xử lý các bẫy dữ liệu (sách thiếu key, số lượng âm) từng bước một, an toàn và cực kỳ dễ bảo trì.

# 4. Luồng xử lý
# Tạo endpoint -> Duyệt danh sách sách -> Bỏ qua sách thiếu quantity hoặc < 0 -> Lọc sách <= 5 -> Trả về kết quả (hoặc mảng rỗng nếu không có).


from fastapi import FastAPI
app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20}
]

@app.get("/books/low-stock")
def get_book_lowstock():
    books_lowstock = []
    result = {
        "message" : "Danh sách sách sắp hết hàng",
        "data" : books_lowstock
    }

    for book in books:
        if book["quantity"] <= 5 and book["quantity"] > 0 :
            books_lowstock.append(book)

    if books_lowstock == []: 
        result["message"] = "Không có sách nào sắp hết hàng"

    return result
# Input: Các Query Parameters tùy chọn trên URL gồm keyword (chuỗi) và max_price (số thực).
# Output: Danh sách sản phẩm (JSON) thỏa mãn điều kiện lọc, hoặc trả về lỗi {"detail": "max_price không được âm"} nếu dữ liệu sai.

# Giải pháp: 
# Sử dụng FastAPI với tham số mặc định là None.
# Dùng hàm .lower() để tìm kiếm không phân biệt chữ hoa/thường.
# Dùng List Comprehension trong Python để duyệt và lọc danh sách.

# Các bước xử lý:
# Bắt lỗi dữ liệu: Trả về lỗi ngay nếu max_price < 0.
# Lọc keyword: Tìm các sản phẩm có chứa từ khóa (nếu có truyền keyword).
# Lọc max_price: Giữ lại các sản phẩm có giá <= max_price (nếu có truyền max_price).
# Trả về kết quả cuối cùng.

from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):
    if max_price is not None and max_price < 0:
        return {"detail": "max_price không được âm"}
    
    result = products
    
    if keyword is not None:
        result = [p for p in result if keyword.lower() in p["name"].lower()]
        
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
        
    return result
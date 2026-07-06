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
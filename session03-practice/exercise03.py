from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Lê Minh Thu",
        "category": "programming",
        "year": 2022,
        "is_available" : True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Phạm Lan Hồng",
        "category": "web",
        "year": 2021,
        "is_available" : False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_available" : False
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_available" : True
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_available" : True
    }
]


@app.get("/books/statistics")
def book_statistics():
    available_books = 0
    borrowed_books = 0
    for book in books:
        if book["is_available"] == True:
            available_books += 1
        else:
            borrowed_books += 1

    return {
        "total_books": len(books),
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }


@app.get("/books/categories")
def book_categories():
    categories = []
    for book in books:
        if book["category"] not in categories:
            categories.append(book["category"])

    return {

  "categories": categories
}


@app.get("/books/latest")
def get_latest():
    if len(books) == 0:
        return {
              "message": "No books available"
            }
    
    latest_book = books[0]
    for book in books:
        if latest_book["year"] < book["year"]:
            latest_book = book

    return latest_book


from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

mock_dt = {}

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    user_id = len(mock_dt) + 1
    user_data = user.model_dump()
    
    user_data["id"] = user_id
    mock_dt[user_id] = user_data
    
    return user_data


# @app.get("/users")
# def get_users():
#     if 
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]

app = FastAPI()

class RoomStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"

class BookingSlot(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"

class RoomCreateRequest(BaseModel):
    code: str = Field(..., description="khong duoc de trong")
    name: str = Field(..., min_length=1, description="khong duoc de trong")
    capacity: int = Field(..., gt=0, description="phai lon hon 0")
    status: RoomStatus

class RoomUpdateRequest(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0, description="phai lon hon 0")
    status: Optional[RoomStatus] = None

class BookingCreateRequest(BaseModel):
    room_id: int
    class_name: str
    student_count: int = Field(..., gt=0, description="phai lon hon 0")
    date: str
    slot: BookingSlot

def check_duplicate_room_code(code):
    for room in rooms:
        if room["code"] == code:
            return room
    return None

def find_room_by_id(room_id):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None

def check_duplicate_booking(room_id, date, slot):
    for booking in room_bookings:
        if booking["room_id"] == room_id and booking["date"] == date and booking["slot"] == slot:
            return booking
    return None

# --- API ROOMS ---
@app.get("/rooms")
def get_rooms(keyword: str = None, status: RoomStatus = None, min_capacity: int = 0):
    filter_room = rooms

    if keyword is not None:
        filter_room = [room for room in filter_room if keyword.lower() in room["code"].lower() or keyword.lower() in room["name"].lower()]

    if status is not None:
        filter_room = [room for room in filter_room if room["status"] == status.value]

    if min_capacity > 0:
        filter_room = [room for room in filter_room if room["capacity"] >= min_capacity]

    return {
        "message": "Lấy danh sách thành công" if len(filter_room) else "Lấy danh sách không thành công",
        "data": filter_room 
    }

@app.post("/rooms")
def create_room(new_room: RoomCreateRequest):
    if check_duplicate_room_code(new_room.code):
        return {
            "message": "Code da ton tai"
        }
    
    room_dict = new_room.model_dump()
    new_id = max([r["id"] for r in rooms], default=0) + 1
    room_dict["id"] = new_id
    
    rooms.append(room_dict)

    return {
        "message": "Them moi phong hoc thanh cong",
        "data": room_dict
    }

@app.get("/rooms/{room_id}")
def detail_room(room_id: int):
    room = find_room_by_id(room_id)
    if room:
        return {
            "message": "Tim thay phong hoc",
            "data": room
        }

    return {
        "message": "Room not found",
    }

@app.put("/rooms/{room_id}")
def update_room(room_id: int, update_room: RoomUpdateRequest):
    room = find_room_by_id(room_id)

    if not room:
        return {
            "message": "Room not found"
        }
    
    if update_room.code is not None and update_room.code != room["code"]:
        if check_duplicate_room_code(update_room.code):
            return {
                "message": "Code da ton tai"
            }        
        room["code"] = update_room.code

    if update_room.name is not None:
        room["name"] = update_room.name

    if update_room.capacity is not None:
        room["capacity"] = update_room.capacity

    if update_room.status is not None:
        room["status"] = update_room.status.value

    return {
        "message": "Cap nhat thanh cong",
        "data": room
    }

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    room = find_room_by_id(room_id)
    if room:
        rooms.remove(room)
        return {
            "message": "Xoa thanh cong",
            "data": room
        }
    
    return {
        "message": "Room not found",
    }

# --- API BOOKINGS ---
@app.get("/room-bookings")
def get_bookings():
    return {
        "message": "Lấy danh sách thành công" if len(room_bookings) else "Lấy danh sách không thành công",
        "data": room_bookings 
    }

@app.post("/room-bookings")
def create_booking(new_booking: BookingCreateRequest):
    # 1. Kiểm tra phòng tồn tại
    room = find_room_by_id(new_booking.room_id)
    if not room:
        return {"message": "Room not found"}
        
    # 2. Kiểm tra trạng thái
    if room["status"] != "AVAILABLE":
        return {"message": "Phong dang khong o trang thai AVAILABLE"}
        
    # 3. Kiểm tra sức chứa
    if new_booking.student_count > room["capacity"]:
        return {"message": "So luong hoc vien vuot qua suc chua cua phong"}
        
    # 4. Kiểm tra đặt trùng lịch
    if check_duplicate_booking(new_booking.room_id, new_booking.date, new_booking.slot.value):
        return {"message": "Phong da duoc dat trong thoi gian va ca hoc nay"}
        
    booking_dict = new_booking.model_dump()
    new_id = max([b["id"] for b in room_bookings], default=0) + 1
    booking_dict["id"] = new_id
    
    room_bookings.append(booking_dict)

    return {
        "message": "Dat lich phong thanh cong",
        "data": booking_dict
    }
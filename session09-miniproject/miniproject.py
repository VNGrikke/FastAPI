from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import re
from enum import Enum

app = FastAPI(
    title="Team Task Management API",
    description="Hệ thống API Quản lý công việc nhóm với chuẩn RESTful API, Validation chặt chẽ và Error Handling tập trung.",
    version="1.0.0"
)

tasks_db = []
max_current_id = 0


class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150, description="Tiêu đề công việc")
    description: str = Field(..., description="Nội dung mô tả")
    assignee: str = Field(..., min_length=2, description="Người thực hiện")
    priority: int = Field(..., ge=1, le=5, description="Mức độ ưu tiên (1-5)")

class TaskUpdateSchema(TaskCreateSchema):
    status: str = Field(..., description="Trạng thái công việc")

class TaskPublicResponse(BaseModel):
    id: int
    title: str
    description: str
    assignee: str
    priority: int
    status: str
    created_at: str

def create_envelope(status_code: int, message: str, data: any = None, error: str = None, path: str = ""):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": path
    }

class BusinessException(Exception):
    def __init__(self, status_code: int, message: str, error_code: str):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_envelope(
            status_code=exc.status_code,
            message=exc.message,
            error=exc.error_code,
            path=request.url.path
        )
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    for error in errors:
        if "loc" in error and "priority" in error["loc"]:
            return JSONResponse(
                status_code=422,
                content=create_envelope(
                    status_code=422,
                    message="Lỗi: Mức độ ưu tiên công việc không hợp lệ (Phải từ 1 đến 5)!",
                    error="ERR-TASK-02: Validation error: Priority field numerical bounds limits constraint violation. Value must be ge=1 and le=5.",
                    path=request.url.path
                )
            )
            
    return JSONResponse(
        status_code=422,
        content=create_envelope(
            status_code=422,
            message="Lỗi: Dữ liệu đầu vào sai định dạng hoặc thiếu trường bắt buộc!",
            error="ERR-VAL-422: Gateway validation error: Input json parameters datatype hints mismatch or core required fields missing.",
            path=request.url.path
        )
    )


@app.get("/tasks/search", status_code=200)
async def search_tasks(request: Request, keyword: Optional[str] = None, status: Optional[str] = None):
    results = []
    
    pattern = re.compile(keyword, re.IGNORECASE) if keyword else None
    
    for task in tasks_db:
        match = True
        
        if pattern:
            if not (pattern.search(task["title"]) or pattern.search(task["assignee"])):
                match = False
                
        if status and task["status"] != status:
            match = False
            
        if match:
            public_data = TaskPublicResponse(**task).model_dump()
            results.append(public_data)
            
    response_data = {
        "total": len(results),
        "items": results
    }
    
    return create_envelope(200, "Tìm kiếm và lọc dữ liệu thành công!", response_data, None, request.url.path)


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreateSchema, request: Request):
    global max_current_id
    
    for t in tasks_db:
        if t["title"].strip().lower() == task.title.strip().lower():
            raise BusinessException(
                status_code=400,
                message="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                error_code="ERR-TASK-01: Task conflict: Title field values duplicates an existing record in the temporary database storage."
            )
            
    max_current_id += 1
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    new_task = {
        "id": max_current_id,
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "priority": task.priority,
        "status": "todo",
        "created_at": created_at,
        "internal_notes": "Tạo mới từ hệ thống API quản lý" 
    }
    
    tasks_db.append(new_task)
    public_data = TaskPublicResponse(**new_task).model_dump()
    
    return JSONResponse(
        status_code=201,
        content=create_envelope(201, "Tạo mới công việc nhóm thành công!", public_data, None, request.url.path)
    )

@app.get("/tasks/{task_id}", status_code=200)
async def get_task_detail(task_id: int, request: Request):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        raise BusinessException(
            status_code=404,
            message="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            error_code="ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope."
        )
        
    public_data = TaskPublicResponse(**task).model_dump()
    return create_envelope(200, "Lấy thông tin chi tiết thành công!", public_data, None, request.url.path)

@app.put("/tasks/{task_id}", status_code=200)
async def update_task(task_id: int, task_update: TaskUpdateSchema, request: Request):
    allowed_statuses = ["todo", "in_progress", "done"]
    if task_update.status not in allowed_statuses:
        raise BusinessException(
            status_code=400,
            message="Lỗi: Trạng thái công việc cập nhật không đúng quy định!",
            error_code="ERR-TASK-03: Business logic error: Invalid task status value. Allowed enumerated selection list: ['todo', 'in_progress', 'done']."
        )
        
    task_idx = next((idx for (idx, t) in enumerate(tasks_db) if t["id"] == task_id), None)
    a
    if task_idx is None:
        raise BusinessException(
            status_code=404,
            message="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            error_code="ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope."
        )
        
    tasks_db[task_idx].update({
        "title": task_update.title,
        "description": task_update.description,
        "assignee": task_update.assignee,
        "priority": task_update.priority,
        "status": task_update.status
    })
    
    public_data = TaskPublicResponse(**tasks_db[task_idx]).model_dump()
    return create_envelope(200, "Cập nhật công việc thành công!", public_data, None, request.url.path)

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    task_idx = next((idx for (idx, t) in enumerate(tasks_db) if t["id"] == task_id), None)
    
    if task_idx is None:
        raise BusinessException(
            status_code=404,
            message="Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            error_code="ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope."
        )
        
    tasks_db.pop(task_idx)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
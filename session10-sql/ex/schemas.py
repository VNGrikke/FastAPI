from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class ResponseAPI(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] | None
    error: Optional[str] | None
    timestamp: datetime = Field(default_factory= datetime.now)
    path: str
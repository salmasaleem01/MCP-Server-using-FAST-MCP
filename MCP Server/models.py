from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    status: TodoStatus = Field(default=TodoStatus.PENDING, description="Todo status")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level (1-5)")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TodoStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=5)


class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoResponse(BaseModel):
    message: str
    todo: Todo


class ErrorResponse(BaseModel):
    detail: str


class StatusUpdate(BaseModel):
    status: TodoStatus

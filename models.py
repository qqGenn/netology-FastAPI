from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Модель входных данных для создания задачи."""
    title: str = Field(..., min_length=3, max_length=100, description="Название задачи")
    description: str | None = Field(default=None, description="Описание задачи")
    priority: int = Field(..., ge=1, le=5, description="Приоритет задачи (1-5)")


class TaskResponse(BaseModel):
    """Модель ответа с данными задачи."""
    id: int
    title: str
    description: str | None = None
    priority: int
    created_at: datetime = Field(..., description="Дата создания задачи в формате ISO 8601")

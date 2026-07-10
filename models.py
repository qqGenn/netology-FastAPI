from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Модель входных данных для создания задачи."""
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название задачи. Обязательное поле, должно содержать от 3 до 100 символов",
        example="Сходить в кино"
    )
    description: str | None = Field(
        default=None,
        description="Подробное описание, что требуется сделать в рамках задачи (опционально)",
        example="Выбрать интересный фильм, купить билеты в последний ряд, взять прохладительные напитки и наслаждаться"
    )
    priority: int = Field(
        ...,
        ge=1,
        le=5,
        description="Уровень приоритета задачи от 1 до 5. 1 - низкий приоритет, 5 - высокий приоритет",
        example=3
    )


class TaskResponse(BaseModel):
    """Модель ответа с данными задачи."""
    id: int = Field(
        ...,
        description="Уникальный идентификатор задачи в системе",
        example=1
    )
    title: str = Field(
        ...,
        description="Название задачи",
        example="Сходить в кино"
    )
    description: str | None = Field(
        default=None,
        description="Подробное описание, что требуется сделать в рамках задачи (опционально)",
        example="Выбрать интересный фильм, купить билеты в последний ряд, взять прохладительные напитки и наслаждаться"
    )
    priority: int = Field(
        ...,
        description="Уровень приоритета задачи от 1 до 5. 1 - низкий приоритет, 5 - высокий приоритет",
        example=3
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания задачи в формате ISO 8601",
        example="2026-07-09T12:00:00.000000Z"
    )

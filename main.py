from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import TaskCreate, TaskResponse
from fastapi.responses import JSONResponse
import json

app = FastAPI(
    title="Task Manager API",
    description="Система управления задачами - Task Manager API",
    version="1.0.0",
    contact={
        "email": "qgen-web@yandex.ru"
    }
)

# Временное хранилище задач
tasks: list[TaskResponse] = []


@app.get(
    "/",
    summary="Root endpoint",
    description="Basic health check endpoint",
    tags=["general"],
    response_description="Successful response"
)
async def root():
    return {"message": "Hello, Netology!"}


@app.post(
    "/tasks",
    status_code=201,
    summary="Создание новой задачи",
    description="Создает новую задачу с указанными параметрами",
    tags=["tasks"],
    response_model=TaskResponse,
    responses={
        422: {
            "description": "Ошибка валидации входных данных",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "loc": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "Путь к полю с ошибкой"
                                        },
                                        "msg": {
                                            "type": "string",
                                            "description": "Описание ошибки"
                                        },
                                        "type": {
                                            "type": "string",
                                            "description": "Тип ошибки валидации"
                                        }
                                    }
                                },
                                "example": [
                                    {
                                        "loc": ["body", "title"],
                                        "msg": "Название задачи обязательно для заполнения и должно содержать от 3 до 100 символов",
                                        "type": "value_error"
                                    },
                                    {
                                        "loc": ["body", "priority"],
                                        "msg": "Приоритет обязателен и должен быть целым числом от 1 до 5",
                                        "type": "value_error"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
)
async def create_task(task: TaskCreate):
    """Создать новую задачу."""
    # Генерируем ID на основе текущего количества задач
    task_id = len(tasks) + 1
    
    # Создаем объект ответа с текущей датой
    task_response = TaskResponse(
        id=task_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        created_at=datetime.now()
    )
    
    # Сохраняем в список
    tasks.append(task_response)
    
    return task_response


@app.get(
    "/tasks/{task_id}",
    summary="Получение данных задачи по task_id",
    description="Возвращает задачу по указанному идентификатору",
    tags=["tasks"],
    response_model=TaskResponse,
    responses={
        404: {
            "description": "Задача с указанным ID не найдена в системе",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                                "example": "Task not found"
                            },
                            "task_id": {
                                "type": "integer",
                                "example": 123
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Ошибка валидации path-параметра",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "loc": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "Путь к полю с ошибкой"
                                        },
                                        "msg": {
                                            "type": "string",
                                            "description": "Описание ошибки"
                                        },
                                        "type": {
                                            "type": "string",
                                            "description": "Тип ошибки валидации"
                                        }
                                    }
                                },
                                "example": [
                                    {
                                        "loc": ["path", "task_id"],
                                        "msg": "task_id должен быть целым числом",
                                        "type": "type_error.integer"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_task(task_id: int):
    """Получить задачу по ID."""
    for task in tasks:
        if task.id == task_id:
            return task
    
    raise HTTPException(
        status_code=404,
        detail={
            "detail": "Task not found",
            "task_id": task_id
        }
    )

from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import TaskCreate, TaskResponse

app = FastAPI(
    title="FastAPI Base Project",
    description="Нетология - FastAPI",
    version="1.0.0"
)

# Временное хранилище задач
tasks: list[TaskResponse] = []


@app.get("/")
async def root():
    return {"message": "Hello, Netology!"}


@app.post("/tasks", status_code=201, response_model=TaskResponse)
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


@app.get("/tasks/{task_id}", response_model=TaskResponse)
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

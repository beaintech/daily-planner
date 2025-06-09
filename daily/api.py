from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from daily.daily_planner.planner import process_tasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://beaintech.github.io", "http://localhost:5173"],
    allow_origins=["http://localhost:5173"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskInput(BaseModel):
    task_name: str
    time_mode: str
    start: Optional[str] = None
    end: Optional[str] = None
    hours: Optional[float] = None
    minutes: Optional[float] = None

@app.post("/process-tasks")
def process_tasks_api(tasks: List[TaskInput]):
    print("🔥 Received tasks:", tasks)
    task_data = [task.dict() for task in tasks]
    print("🔥 Converted task_data:", task_data)
    result = process_tasks(task_data)
    return result

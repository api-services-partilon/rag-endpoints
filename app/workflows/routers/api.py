from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.workflows.agent import agent
from agents import Runner
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/workflows", tags=["workflows"])

class ProjectDescription(BaseModel):
    description: str

@router.post("/create")
async def create(projectDescription: ProjectDescription):
    try:
        description = f"{projectDescription.description}"
        result = await Runner.run(agent, description)

        tasks = result.final_output

        parsed_tasks = []
        for task in tasks:
            try:
                parsed_date = datetime.strptime(task.due_date, "%Y-%m-%d")
                parsed_tasks.append({
                    "name": task.name,
                    "status": task.status,
                    "due_date": parsed_date.strftime("%Y-%m-%d")
                })
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date format in task: {task.due_date}"
                )
        return JSONResponse(content={"tasks": parsed_tasks}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.workflows.agent import agent
from agents import Runner
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/workflows", tags=["workflows"])

class ProjectDescription(BaseModel):
    description: str
    assignee: str

@router.post("/create")
async def create(projectDescription: ProjectDescription):
    try:
        description = f"{projectDescription.description} + assignee: {projectDescription.assignee}"
        result = await Runner.run(agent, description)
        print(datetime.now())
        return JSONResponse(content={"tasks": result.final_output.dict()}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
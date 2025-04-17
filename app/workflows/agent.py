from pydantic import BaseModel
from typing import List
from agents import Agent

PROMPT = (
    "You are an agent who helps create tasks for projects based on project descriptions."
    "Your duties include analyzing the project description and creating a list of tasks."
    "The task components include:"
    "- Task Name"
    "- Task Description"
    "- Task Assignee (is the person who inserted the project description)"
    "- Task Status"
)

class TaskOutput(BaseModel):
    name: str
    description: str
    assignee: str
    status: str

class TaskOutputItem(BaseModel):
    task: List[TaskOutput]

agent = Agent(
    name="task_creator_agent",
    instructions=PROMPT,
    output_type=TaskOutputItem,
)
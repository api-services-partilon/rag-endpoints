from pydantic import BaseModel
from typing import List
from enum import Enum
from agents import Agent

PROMPT = (
    "You are an AI assistant that helps create tasks for a project based on a provided project description. "
    "Your job is to analyze the description and generate a clear list of tasks. "
    "Each task should include the following fields:\n"
    "- Task Name\n"
    "- Task Status (choose from: BACKLOG, IN_PROGRESS, IN_REVIEW, TODO, DONE)\n"
    "- Due Date (set to one week from today's date)\n\n"
    "Please return the tasks in a structured JSON format, as a list of objects with the specified fields."
)

class TaskStatus(str, Enum):
    BACKLOG = "BACKLOG"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    TODO = "TODO"
    DONE = "DONE"

class TaskOutput(BaseModel):
    name: str
    status: TaskStatus
    due_date: str

agent = Agent(
    name="task_creator_agent",
    instructions=PROMPT,
    output_type=List[TaskOutput],
)

from pydantic import BaseModel

from typing import Dict

class Resource(BaseModel):
    resourcesName: str
    method: str
    description: str

class Resources(BaseModel):
    __root__: Dict[int, Resource]

class Content(BaseModel):
    description: str
    resources: Resources
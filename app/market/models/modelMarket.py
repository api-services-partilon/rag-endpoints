from pydantic import BaseModel, RootModel

from typing import Dict

class Resource(BaseModel):
    resourcesName: str
    method: str
    description: str

class Resources(RootModel[Dict[int, Resource]]):
    pass

class Content(BaseModel):
    description: str
    resources: Resources

class TranslateContent(BaseModel):
    language: str
    content: Content
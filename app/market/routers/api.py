import json
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.libs.openai import getTransaltedText

router = APIRouter(prefix="/market", tags=["market"])

@router.post("/translate")
def translate(init: dict , target: str):
    response = getTransaltedText(init, target)
    transaltedJson = json.loads(response)
    return transaltedJson
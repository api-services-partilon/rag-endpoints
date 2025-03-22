import json
from fastapi import APIRouter

from app.libs.openai import getTransaltedText
from app.market.models.modelMarket import TranslateContent

router = APIRouter(prefix="/market", tags=["market"])

@router.post("/translate")
def translate(content: TranslateContent):
    response = getTransaltedText(content)
    transaltedJson = json.loads(response["arguments"])
    return {"message": "Data translated successfully", "data": transaltedJson}
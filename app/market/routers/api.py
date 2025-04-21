from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.market.agent import useAgents

router = APIRouter(prefix="/market", tags=["market"])

class TranslateRequest(BaseModel):
    language: str
    content: dict

@router.post("/translate")
async def translate(request: TranslateRequest):
    try:
        convert = f'"{request}"'
        translation = await useAgents(convert)
        return JSONResponse(content={"translation": translation}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from agents import Runner
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.customers.agents import financials_agent

router = APIRouter(prefix="/customers", tags=["customers"])  

class RequestDict(BaseModel):
    message: str

@router.post("/summary")
async def get_specific_data(content: RequestDict):
    try:
        result = await Runner.run(financials_agent, content.message)
        return JSONResponse(content={"summary": result.final_output.dict()}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
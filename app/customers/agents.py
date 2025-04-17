from pydantic import BaseModel

from agents import Agent

FINANCIALS_PROMPT = (
    "You are a helpful financial assistant. Based on the following summary, provide a clear, human-friendly insight."
    "Analyze the trend, give useful advice, and include any interesting observations related to income, expenses, and remaining balance."
    "Mention percentages, savings rates, or potential budget improvements if relevant."
)

class SummaryModel(BaseModel):
    reply: str

financials_agent = Agent(
    name="FundamentalsAnalystAgent",
    instructions=FINANCIALS_PROMPT,
    output_type=SummaryModel,
)
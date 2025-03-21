from openai import OpenAI
from fastapi import HTTPException

from app.config import settings

openaiSk = settings.openai_api_key
if not openaiSk:
    raise ValueError("API keys for OpenAI must be set in environment variables.")

openai = OpenAI(api_key=openaiSk)

def getEmbedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    embeddingData = response.data[0].embedding

    if embeddingData is None:
        raise HTTPException(status_code=404, detail="Embedding not found")

    return embeddingData
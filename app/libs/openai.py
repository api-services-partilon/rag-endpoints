from typing import Any
from openai import OpenAI
from fastapi import HTTPException
from pydantic import Json

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

def getTransaltedText(content: Json[Any], language: str):
    prompt = f"Translate this JSON {content} to {language}. " \
            "If the language is shorter than 4 characters, check if there is any country code with the same characters. " \
            "If you cannot translate, respond with 'cannot translate'."
    response = openai.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[{
            "role": "system",
            "content": prompt
        }]
    )

    translatedText = response.choices[0].message.content

    if translatedText is None:
        raise HTTPException(status_code=404, detail="Translation not found")

    return translatedText
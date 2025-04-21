from openai import OpenAI
from fastapi import HTTPException

from app.config import settings

openaiSk = settings.openai_api_key
if not openaiSk:
    raise ValueError("API keys for OpenAI must be set in environment variables.")

openai = OpenAI(api_key=openaiSk)

def getEmbedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )

    embeddingData = response.data[0].embedding

    if embeddingData is None:
        raise HTTPException(status_code=404, detail="Embedding not found")

    return embeddingData

workflowTools = [{
    "type": "function",
    "name": "createNote",
    "description": "Create a note",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The user question or search query."
            },
            "options": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the note."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content of the note."
                    }
                }
            }
        }
    }
}]

def getAgent(description: str):
    response = openai.responses.create(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": description
        }],
        tools=workflowTools
    )

    return response.output
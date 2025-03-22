from typing import Any
from openai import OpenAI
from fastapi import HTTPException
from pydantic import Json

from app.config import settings
from app.market.models.modelMarket import TranslateContent

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

translateTools = [{
    "type": "function",
    "name": "translated-text",
    "description": "Translate a text into a target language and check if the language matches the ISO 639-1 or ISO 639-2 or ISO Language Names.",
    "parameters": {
        "type": "object",
        "properties": {
            "content": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The description of the content and the target text to be translated."
                    },
                    "resources": {
                        "type": "object",
                        "properties": {
                            "resourcesName": {
                                "type": "string",
                                "description": "The name of the resource."
                            },
                            "method": {
                                "type": "string",
                                "description": "The method of the resource."
                            },
                            "description": {
                                "type": "string",
                                "description": "The description of the resource and the target text to be translated."
                            }
                        }
                    }
                }
            },
            "language": {
                "type": "string",
                "description": "The target language to translate to."
            }
        },
        "required": ["content", "language"]
    }
}]

def getTransaltedText(content: TranslateContent):
    response = openai.responses.create(
        model="gpt-4o",
        input=[{
            "role": "system",
            "content": content.model_dump_json()
        }],
        tools=translateTools
    )

    translatedText = response.output

    if translatedText is None:
        raise HTTPException(status_code=404, detail="Translation not found")

    return translatedText

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
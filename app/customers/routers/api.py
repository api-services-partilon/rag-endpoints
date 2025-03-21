from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.customers.libs.openai import getEmbedding
from app.customers.libs.pinecone import pinecone_index
from app.customers.models.modelCustomers import Transaction

router = APIRouter(prefix="/customer_data", tags=["customer_data"])

async def getEmbeddingData(transaction: Transaction):
    response = getEmbedding(transaction.categoryId + " " + transaction.payee + " " + str(transaction.amount) + " " + transaction.notes + " " + transaction.accountId)
    return response

@router.post("/store_data")
async def store_data(record: Transaction):
    embeddingData = await getEmbeddingData(record)
    try:
        pinecone_index.upsert(
            namespace= "ns1",
            vectors=[
                {
                    "id": record.id,
                    "values": embeddingData,
                    "metadata": {
                        "date": record.date.timestamp(),
                        "category": record.category,
                        "payee": record.payee,
                        "account": record.account
                    }
                }
            ]
        )
        return {"message": "Data stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@router.post("/specific_data")
async def get_specific_data(start_date: datetime, end_date: datetime, input: str):
    try:
        embeddingData = getEmbedding(input)
        print(start_date.timestamp() , end_date.timestamp())
        response = pinecone_index.query(
            namespace="ns1",
            vector=embeddingData,
            top_k=10000,
            filter={
                "date": {
                    "$gte": start_date.timestamp(),
                    "$lte": end_date.timestamp()
                }
            },
            include_metadata=True,
            include_values=False
        )
        response_dict = response.to_dict()
        response_encode = jsonable_encoder(response_dict)
        return JSONResponse(content=response_encode['matches'], status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
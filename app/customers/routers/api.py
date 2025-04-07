from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.libs.openai import getEmbedding
from app.libs.pinecone import pinecone_index
from app.customers.models.modelCustomers import Transaction

router = APIRouter(prefix="/customers", tags=["customers"])

async def getEmbeddingData(transaction: Transaction):
    try:
        response = getEmbedding(transaction.categoryId + " " + transaction.category + " " + transaction.payee + " " + transaction.notes + " " + transaction.accountId + " " + transaction.account)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert")
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
                        "accountId": record.accountId,
                        "date": record.date.timestamp(),
                        "amount": record.amount
                    }
                }
            ]
        )
        return JSONResponse(content={"message": "Data stored successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@router.post("/summary")
async def get_specific_data(start_date: datetime, end_date: datetime, accountId: str):
    try:
        embeddingData = getEmbedding(accountId)
        response = pinecone_index.query(
            namespace="ns1",
            top_k=100,
            vector=embeddingData,
            filter={
                "accountId": accountId,
                "date": {
                    "$gte": start_date.timestamp(),
                    "$lte": end_date.timestamp()
                }
            },
            include_metadata=True,
            include_values=False
        )
        
        matches = response.to_dict().get("matches", [])
        print(matches)
        filtered_matches = [match for match in matches if match["score"] > 0.8]
        print(filtered_matches)
        income = sum(m["metadata"]["amount"] for m in filtered_matches if m["metadata"]["amount"] > 0)
        expenses = sum(m["metadata"]["amount"] for m in filtered_matches if m["metadata"]["amount"] < 0)
        remaining = income + expenses
        
        return JSONResponse(content={
            "summary": {
                "income": round(income, 2),
                "expenses": round(expenses, 2),
                "remaining": round(remaining, 2)
            }
        } , status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from pydantic import BaseModel

from typing import List
from datetime import datetime

class customerEmbeddingData(BaseModel):
    id: str
    metadata: dict
    score: float
    sparse_values: dict
    values: List[float]

class customerEmbeddingResponse(BaseModel):
    matches: List[customerEmbeddingData]
    namespace: str

class Transaction(BaseModel):
    id: str
    date: datetime
    category: str
    categoryId: str
    payee: str
    amount: float
    notes: str
    account: str
    accountId: str

class Transactions(BaseModel):
    transactions: List[Transaction]
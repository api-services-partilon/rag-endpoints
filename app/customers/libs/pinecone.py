from pinecone.grpc import PineconeGRPC as Pinecone

from app.config import settings

pineconeSk = settings.pinecone_api_key
if not pineconeSk:
    raise ValueError("API keys for Pinecone must be set in environment variables.")

pinecone = Pinecone(api_key=pineconeSk)
index_name = "customer-data-platform"
pinecone_index = pinecone.Index(index_name)
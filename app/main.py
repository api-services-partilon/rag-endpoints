from fastapi import FastAPI
from app.customers.routers import api as customerRoutes

app = FastAPI()

app.include_router(customerRoutes.router)
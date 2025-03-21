from fastapi import FastAPI
from app.customers.routers import api as customerRoutes
from app.market.routers import api as marketRoutes

app = FastAPI()

app.include_router(customerRoutes.router)
app.include_router(marketRoutes.router)
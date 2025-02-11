from fastapi import FastAPI, HTTPException, Depends

from app.routers import data_sources
from app.routers import transaction_source_categories
from app.routers import transaction_sources
from app.routers import financial_transactions
from app.routers import upload_transactions
from app.routers import list_router

from app.database import initialize_database

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    await initialize_database()

@app.get("/ping")
async def read_root():
    return {"message": "Pong"}

app.include_router(data_sources.router)
app.include_router(transaction_source_categories.router)
app.include_router(transaction_sources.router)
app.include_router(financial_transactions.router)   
app.include_router(upload_transactions.router)
app.include_router(list_router.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволити всі джерела (можете обмежити конкретними доменами)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

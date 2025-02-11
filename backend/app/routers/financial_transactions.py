from fastapi import APIRouter, Query, Depends
from app.services.financial_transactions_service import FinancialTransactionService
from app.schemas.financial_transaction import FinancialTransactionCreate, FinancialTransactionUpdate

router = APIRouter(prefix="/financial-transactions", tags=["Financial Transactions"])

@router.get("/")
async def get_transactions(
    page: int = Query(1),
    sort: str = Query("date"),
    order: str = Query("asc"),
    start_date: str = Query(None),
    end_date: str = Query(None),
    source: str = Query(None),
    category: str = Query(None),
    bank: str = Query(None),
    min_amount: float = Query(None),
    max_amount: float = Query(None),
    service: FinancialTransactionService = Depends(FinancialTransactionService)
):
    return await service.get_all(page, sort, order, start_date, end_date, source, category, bank, min_amount, max_amount)

@router.post("/")
async def create(data: FinancialTransactionCreate, service: FinancialTransactionService = Depends(FinancialTransactionService)):
    return await service.create(data)

@router.put("/{transaction_id}")
async def update(transaction_id: int, data: FinancialTransactionUpdate, service: FinancialTransactionService = Depends(FinancialTransactionService)):
    return await service.update(transaction_id, data)

@router.delete("/{transaction_id}")
async def delete(transaction_id: int, service: FinancialTransactionService = Depends(FinancialTransactionService)):
    return await service.delete(transaction_id)

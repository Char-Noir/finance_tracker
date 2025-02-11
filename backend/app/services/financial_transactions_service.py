from app.repositories.financial_transactions_repository import *
from app.schemas.financial_transaction import *
from fastapi import HTTPException, Depends

class FinancialTransactionService:
    def __init__(self, repository: FinancialTransactionRepository = Depends(FinancialTransactionRepository)):
        self.repository = repository

    async def get_all(self, 
        page: int,
        sort: str,
        order: str,
        start_date: str,
        end_date: str,
        source: str,
        category: str,
        bank: str,
        min_amount: float,
        max_amount: float):
        return await self.repository.get_all(page, sort, order, start_date, end_date, source, category, bank, min_amount, max_amount)

    async def create(self, data: FinancialTransactionCreate):
        return await self.repository.create(data)

    async def update(self, transaction_id: int, data: FinancialTransactionUpdate):
        return await self.repository.update(transaction_id, data)

    async def delete(self, transaction_id: int):
        return await self.repository.delete(transaction_id)

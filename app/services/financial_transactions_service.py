from app.repositories.financial_transactions_repository import FinancialTransactionRepository
from app.schemas.financial_transaction import FinancialTransactionCreate, FinancialTransactionUpdate, FinancialTransactionSchema
from app.database import SessionLocal
from app.services.data_sources_service import ServiceException

class FinancialTransactionService:
    async def _create_repository(self):
        db = SessionLocal()
        return FinancialTransactionRepository(db), db

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
        repository, db = await self._create_repository()
        async with db:
            # This method already returns a dict, which is what the template expects.
            # No changes needed here for now.
            return await repository.get_all(page, sort, order, start_date, end_date, source, category, bank, min_amount, max_amount)

    async def create(self, data: FinancialTransactionCreate):
        repository, db = await self._create_repository()
        async with db:
            db_object = await repository.create(data)
            return FinancialTransactionSchema.from_orm(db_object)

    async def update(self, transaction_id: int, data: FinancialTransactionUpdate):
        repository, db = await self._create_repository()
        async with db:
            try:
                db_object = await repository.update(transaction_id, data)
                return FinancialTransactionSchema.from_orm(db_object)
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

    async def delete(self, transaction_id: int):
        repository, db = await self._create_repository()
        async with db:
            try:
                await repository.delete(transaction_id)
                return None
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, exists
from sqlalchemy.sql import func
from app.schemas.financial_transaction import FinancialTransactionCreate, FinancialTransactionUpdate
from sqlalchemy.orm import joinedload
from app.models.transaction_sources import TransactionSource
from app.models.financial_transaction import FinancialTransaction

class FinancialTransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self,
        page: int = 1,
        sort: str = "date",
        order: str = "asc",
        start_date: str = None,
        end_date: str = None,
        source: str = None,
        category: str = None,
        bank: str = None,
        min_amount: float = None,
        max_amount: float = None
    ):
        query = select(FinancialTransaction).options(
            joinedload(FinancialTransaction.source).joinedload(TransactionSource.category),
            joinedload(FinancialTransaction.data_source)
        )

        if start_date:
            query = query.where(FinancialTransaction.date >= start_date)
        if end_date:
            query = query.where(FinancialTransaction.date <= end_date)
        if source:
            query = query.where(FinancialTransaction.source_id == source)
        if category:
            query = query.where(TransactionSource.category_id == category)
        if bank:
            query = query.where(FinancialTransaction.data_source_id == bank)
        if min_amount is not None and max_amount is not None:
            query = query.where(FinancialTransaction.amount.between(min_amount, max_amount))

        if order not in ["asc", "desc"]:
            order = "asc"
        if sort == "date":
            query = query.order_by(getattr(FinancialTransaction.date, order)())
        elif sort == "source":
            query = query.order_by(getattr(FinancialTransaction.source_id, order)())
        elif sort == "category":
            query = query.order_by(getattr(TransactionSource.category_id, order)())
        elif sort == "bank":
            query = query.order_by(getattr(FinancialTransaction.data_source_id.name, order)())
        elif sort == "amount":
            query = query.order_by(getattr(FinancialTransaction.amount, order)())
        
        count_query = query.with_only_columns(func.count()).order_by(None)
        total_count = (await self.db.execute(count_query)).scalar()
        
        page_size = 10
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        transactions = result.scalars().all()

        return {
            "transactions": [
                {
                    "id": transaction.id,
                    "date": transaction.date,
                    "source_name": transaction.source.alt_name if transaction.source else None,
                    "category_name": transaction.source.category.name if transaction.source and transaction.source.category else None,
                    "data_source_name": transaction.data_source.name if transaction.data_source else None,
                    "amount": transaction.amount,
                }
                for transaction in transactions
            ],
            "total_pages": (total_count // page_size) + (1 if total_count % page_size else 0),
            "current_page": page,
        }
    
    async def get_by_id(self, transaction_id: int):
        query = (
            select(FinancialTransaction)
            .options(
                joinedload(FinancialTransaction.source).joinedload(TransactionSource.category),
                joinedload(FinancialTransaction.data_source)
            )
            .where(FinancialTransaction.id == transaction_id)
        )
        result = await self.db.execute(query)
        transaction = result.scalars().first()

        if not transaction:
            raise ValueError("Financial transaction not found")

        return {
            "id": transaction.id,
            "date": transaction.date,
            "details": transaction.details,
            "source_id": transaction.source_id,
            "source_name": transaction.source.alt_name if transaction.source else None,
            "category_name": transaction.source.category.name if transaction.source and transaction.source.category else None,
            "data_source_id": transaction.data_source_id,
            "data_source_name": transaction.data_source.name if transaction.data_source else None,
            "mcc": transaction.mcc,
            "amount": transaction.amount,
            "currency": transaction.currency,
        }

    async def create(self, data: FinancialTransactionCreate):
        transaction = FinancialTransaction(**data.dict())
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def update(self, transaction_id: int, data: FinancialTransactionUpdate):
        transaction = await self.db.get(FinancialTransaction, transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(transaction, key, value)
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def delete(self, transaction_id: int):
        transaction = await self.db.get(FinancialTransaction, transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        await self.db.delete(transaction)
        await self.db.commit()

    async def exists(self, data_source_id: int, source_id: int, date: str):
        result = await self.db.execute(
            select(FinancialTransaction)
            .where(
                FinancialTransaction.data_source_id == data_source_id,
                FinancialTransaction.source_id == source_id,
                FinancialTransaction.date == date
            )
        )
        return result.scalars().first() is not None
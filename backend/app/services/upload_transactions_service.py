from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from fastapi import Depends, HTTPException
from app.repositories.financial_transactions_repository import FinancialTransactionRepository
from app.repositories.transaction_sources_repository import TransactionSourceRepository
from app.models.financial_transaction import FinancialTransaction
import pandas as pd
from datetime import datetime
from app.schemas.transaction_sources import TransactionSourceCreate

def get_session_local():
    yield SessionLocal()

class UploadTransactionsService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_session_local),
        transaction_repo: FinancialTransactionRepository = Depends(),
        source_repo: TransactionSourceRepository = Depends()
    ):
        self.db = db
        self.transaction_repo = transaction_repo
        self.source_repo = source_repo

    async def process_csv(self, data_source_id: int, df: pd.DataFrame):
        async with self.db.begin():
            for index, row in df.iterrows():
                # Обробка рядка
                try:
                    details = row["Деталі операції"]
                    date_str = row["Дата i час операції"]
                    amount = row["Сума в валюті картки (UAH)"]
                    currency = row["Валюта"]

                    try:
                        date = datetime.strptime(date_str.strip(), "%d.%m.%Y %H:%M:%S")
                    except ValueError:
                        raise ValueError(f"Неправильна дата в рядку {index + 1}: {date_str}")

                    # Знаходимо джерело фінансового руху
                    source = await self.source_repo.get_by_details(details)
                    if not source:
                        # Якщо джерело не знайдено, створюємо нове з категорією 0
                       source = await self.source_repo.create(
                        TransactionSourceCreate(name=details, alt_name=None, category_id=0)
                        )

                    # Перевіряємо унікальність
                    exists = await self.transaction_repo.exists(data_source_id, source.id, date)
                    if exists:
                        continue  # Пропускаємо дублікат

                    # Додаємо транзакцію
                    transaction = FinancialTransaction(
                        date=date,
                        details=details,
                        source_id=source.id,
                        data_source_id=data_source_id,
                        mcc=row.get("MCC"),
                        amount=amount,
                        currency=currency
                    )
                    self.db.add(transaction)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Помилка в рядку {index + 1}: {str(e)}")

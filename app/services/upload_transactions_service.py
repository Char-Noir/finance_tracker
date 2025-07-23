from app.database import SessionLocal
from app.repositories.financial_transactions_repository import FinancialTransactionRepository
from app.repositories.transaction_sources_repository import TransactionSourceRepository
from app.models.financial_transaction import FinancialTransaction
import pandas as pd
from datetime import datetime
from app.schemas.transaction_sources import TransactionSourceCreate
from app.services.data_sources_service import ServiceException

class UploadTransactionsService:
    def __init__(self):
        self.db = SessionLocal()
        self.transaction_repo = FinancialTransactionRepository()
        self.source_repo = TransactionSourceRepository()

    async def process_csv(self, data_source_id: int, df: pd.DataFrame):
        async with self.db.begin():
            for index, row in df.iterrows():
                try:
                    details = row["Деталі операції"]
                    date_str = row["Дата i час операції"]
                    amount = row["Сума в валюті картки (UAH)"]
                    currency = row["Валюта"]

                    try:
                        date = datetime.strptime(date_str.strip(), "%d.%m.%Y %H:%M:%S")
                    except ValueError:
                        raise ValueError(f"Неправильна дата в рядку {index + 1}: {date_str}")

                    source = await self.source_repo.get_by_details(details)
                    if not source:
                       source = await self.source_repo.create(
                        TransactionSourceCreate(name=details, alt_name=None, category_id=None)
                        )

                    exists = await self.transaction_repo.exists(data_source_id, source.id, date)
                    if exists:
                        continue

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
                    raise ServiceException(message=f"Помилка в рядку {index + 1}: {str(e)}", status_code=400)
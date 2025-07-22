from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FinancialTransactionBase(BaseModel):
    date: datetime
    details: str
    source_id: int
    data_source_id: int
    mcc: Optional[int]
    amount: float
    currency: str

class FinancialTransactionCreate(FinancialTransactionBase):
    pass

class FinancialTransactionUpdate(FinancialTransactionBase):
    pass

class FinancialTransactionSchema(FinancialTransactionBase):
    id: int

    class Config:
        from_attributes = True
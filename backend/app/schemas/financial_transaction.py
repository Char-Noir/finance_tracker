from pydantic import BaseModel
from typing import Optional

class FinancialTransactionBase(BaseModel):
    date: str
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

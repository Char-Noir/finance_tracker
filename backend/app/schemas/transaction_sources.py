from pydantic import BaseModel
from typing import Optional

class TransactionSourceBase(BaseModel):
    name: str
    alt_name: Optional[str] = None
    category_id: Optional[int] = None

class TransactionSourceCreate(TransactionSourceBase):
    pass

class TransactionSourceUpdate(TransactionSourceBase):
    pass

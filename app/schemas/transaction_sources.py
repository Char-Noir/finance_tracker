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

class TransactionSourceSchema(TransactionSourceBase):
    id: int
    category_name: Optional[str] = None # To hold the category name

    class Config:
        from_attributes = True
from pydantic import BaseModel

class TransactionSourceCategoryBase(BaseModel):
    name: str
    color: str

class TransactionSourceCategoryCreate(TransactionSourceCategoryBase):
    pass

class TransactionSourceCategoryUpdate(TransactionSourceCategoryBase):
    pass

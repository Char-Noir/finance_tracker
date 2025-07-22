from pydantic import BaseModel

class TransactionSourceCategoryBase(BaseModel):
    name: str
    color: str

class TransactionSourceCategoryCreate(TransactionSourceCategoryBase):
    pass

class TransactionSourceCategoryUpdate(TransactionSourceCategoryBase):
    pass

class TransactionSourceCategorySchema(TransactionSourceCategoryBase):
    id: int

    class Config:
        from_attributes = True
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator

class TransactionSourceBase(BaseModel):
    name: str
    alt_name: Optional[str] = None
    category_id: Optional[Union[int, str]] = None

    @field_validator('category_id', mode='before')
    @classmethod
    def convert_category_id(cls, v):
        if v == '':
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                raise ValueError("category_id must be an integer or an empty string")
        return v

class TransactionSourceCreate(TransactionSourceBase):
    pass

class TransactionSourceUpdate(TransactionSourceBase):
    pass

class TransactionSourceSchema(TransactionSourceBase):
    id: int
    category_name: Optional[str] = None # To hold the category name

    class Config:
        from_attributes = True

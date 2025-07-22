from pydantic import BaseModel
from datetime import datetime

class ListBase(BaseModel):
    name: str
    author: str

class ListCreateRequest(ListBase):
    pass

class ListUpdateRequest(BaseModel):
    name: str

class ListSchema(ListBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

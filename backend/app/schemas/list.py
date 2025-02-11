from pydantic import BaseModel

class ListCreateRequest(BaseModel):
    name: str
    author: str

class ListUpdateRequest(BaseModel):
    name: str
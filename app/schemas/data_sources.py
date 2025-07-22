from pydantic import BaseModel

class DataSourceBase(BaseModel):
    name: str

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(DataSourceBase):
    pass

class DataSourceSchema(DataSourceBase):
    id: int

    class Config:
        from_attributes = True
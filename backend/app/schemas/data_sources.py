from pydantic import BaseModel

class DataSourceBase(BaseModel):
    name: str

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(DataSourceBase):
    pass

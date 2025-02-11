from app.repositories.data_sources_repository import DataSourceRepository
from app.schemas.data_sources import DataSourceCreate, DataSourceUpdate
from fastapi import HTTPException, Depends

class DataSourceService:
    def __init__(self, repository: DataSourceRepository = Depends(DataSourceRepository)):
        self.repository = repository

    async def get_all_data_sources(self):
        return await self.repository.get_all()
    async def get_all_data_sources_sh(self):
        return await self.repository.get_all_short()

    async def create_data_source(self, data: DataSourceCreate):
        if len(data.name) < 3:
            raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
        if await self.repository.exists_by_name(data.name):
            raise HTTPException(status_code=400, detail="Data source with this name already exists")
        return await self.repository.create(data)

    async def update_data_source(self, data_source_id: int, data: DataSourceUpdate):
        if len(data.name) < 3:
            raise HTTPException(status_code=400, detail="Name must be at least 3 characters long")
        if await self.repository.exists_by_name_and_not_id(data.name, data_source_id):
            raise HTTPException(status_code=400, detail="Data source with this name already exists")
        return await self.repository.update(data_source_id, data)

    async def delete_data_source(self, data_source_id: int):
        if await self.repository.is_used_as_foreign_key(data_source_id):
            raise HTTPException(status_code=400, detail="Data source is used as a foreign key and cannot be deleted")
        return await self.repository.delete(data_source_id)

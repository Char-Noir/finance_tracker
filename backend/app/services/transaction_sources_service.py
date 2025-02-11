from app.repositories.transaction_sources_repository import *
from app.schemas.transaction_sources import *
from fastapi import HTTPException, Depends

class TransactionSourceService:
    def __init__(self, repository: TransactionSourceRepository = Depends(TransactionSourceRepository)):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def get_all_sh(self):
        return await self.repository.get_all_short()

    async def create(self, data: TransactionSourceCreate):
        return await self.repository.create(data)

    async def update(self, source_id: int, data: TransactionSourceUpdate):
        return await self.repository.update(source_id, data)

    async def delete(self, source_id: int):
        return await self.repository.delete(source_id)

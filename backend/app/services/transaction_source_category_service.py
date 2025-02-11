from app.repositories.transaction_source_category_repository import TransactionSourceCategoryRepository
from app.schemas.transaction_source_category import TransactionSourceCategoryCreate, TransactionSourceCategoryUpdate
from fastapi import HTTPException, Depends

class TransactionSourceCategoryService:
    def __init__(self, repository: TransactionSourceCategoryRepository = Depends(TransactionSourceCategoryRepository)):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()
    
    async def get_all_sh(self):
        return await self.repository.get_all_short()

    async def create(self, data: TransactionSourceCategoryCreate):
        return await self.repository.create(data)

    async def update(self, category_id: int, data: TransactionSourceCategoryUpdate):
        return await self.repository.update(category_id, data)

    async def delete(self, category_id: int):
        return await self.repository.delete(category_id)

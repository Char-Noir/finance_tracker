from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.repositories.list_repository import ListRepository

class ListService:
    def __init__(self, repository: ListRepository = Depends(ListRepository)):
        self.repository = repository

    async def get_all(self, page: int, size: int, sort_by: str, order: str):
        return await self.repository.get_all(page, size, sort_by, order)

    async def get_by_id(self, list_id: int):
        return await self.repository.get_by_id(list_id)

    async def create(self, name: str, author: str):
        return await self.repository.create(name, author)

    async def update(self, list_id: int, name: str):
        return await self.repository.update(list_id, name)

    async def delete(self, list_id: int):
        return await self.repository.delete(list_id)
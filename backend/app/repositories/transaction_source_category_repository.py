from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, exists
from app.schemas.transaction_source_category import TransactionSourceCategoryCreate, TransactionSourceCategoryUpdate
from fastapi import Depends
from app.database import SessionLocal
from fastapi import FastAPI, HTTPException, Depends
from app.models.transaction_source_category import TransactionSourceCategory

def get_session_local():
    yield SessionLocal()

class TransactionSourceCategoryRepository:
    def __init__(self, db: AsyncSession = Depends(get_session_local)):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(TransactionSourceCategory))
        return result.scalars().all()
    
    async def get_all_short(self):
        """
        Get all unique transaction source categories.
        """
        query = select(TransactionSourceCategory.id, TransactionSourceCategory.name).distinct()
        result = await self.db.execute(query)
        return [{"id": row.id, "name": row.name} for row in result]

    async def create(self, data: TransactionSourceCategoryCreate):
        new_category = TransactionSourceCategory(**data.dict())
        self.db.add(new_category)
        await self.db.commit()
        await self.db.refresh(new_category)
        return new_category

    async def update(self, category_id: int, data: TransactionSourceCategoryUpdate):
        category = await self.db.get(TransactionSourceCategory, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(category, key, value)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category_id: int):
        category = await self.db.get(TransactionSourceCategory, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.db.delete(category)
        await self.db.commit()

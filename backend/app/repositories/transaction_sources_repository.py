from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, exists
from sqlalchemy.orm import joinedload
from app.models.transaction_sources import *
from app.schemas.transaction_sources import *
from fastapi import Depends
from app.database import SessionLocal
from fastapi import FastAPI, HTTPException, Depends

def get_session_local():
    yield SessionLocal()

class TransactionSourceRepository:
    def __init__(self, db: AsyncSession = Depends(get_session_local)):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(TransactionSource).options(joinedload(TransactionSource.category))
        )
        return [
            {
                "id": source.id,
                "name": source.name,
                "alt_name": source.alt_name,
                "category_id": source.category_id,
                "category_name": source.category.name if source.category else None
            }
            for source in result.scalars().all()
        ]
    
    async def get_all_short(self):
        """
        Get all unique transaction sources.
        """
        query = select(TransactionSource.id, TransactionSource.alt_name).distinct()
        result = await self.db.execute(query)
        return [{"id": row.id, "name": row.alt_name} for row in result]

    async def create(self, data: TransactionSourceCreate):
        new_source = TransactionSource(**data.dict())
        self.db.add(new_source)
        await self.db.commit()
        await self.db.refresh(new_source)
        return new_source

    async def update(self, source_id: int, data: TransactionSourceUpdate):
        source = await self.db.get(TransactionSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(source, key, value)
        self.db.add(source)
        await self.db.commit()
        await self.db.refresh(source)
        return source

    async def delete(self, source_id: int):
        source = await self.db.get(TransactionSource, source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        await self.db.delete(source)
        await self.db.commit()
    async def get_by_details(self, details: str):
        """
        Find a transaction source by exact match of trimmed details.
        """
        details = details.strip()  # Обрізаємо пробіли
        result = await self.db.execute(
            select(TransactionSource).where(TransactionSource.name == details)
        )
        return result.scalars().first()
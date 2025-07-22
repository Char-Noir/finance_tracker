from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.transaction_sources import TransactionSource
from app.schemas.transaction_sources import TransactionSourceCreate, TransactionSourceUpdate

class TransactionSourceRepository:
    def __init__(self, db: AsyncSession):
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
            raise ValueError("Source not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(source, key, value)
        self.db.add(source)
        await self.db.commit()
        await self.db.refresh(source)
        return source

    async def delete(self, source_id: int):
        source = await self.db.get(TransactionSource, source_id)
        if not source:
            raise ValueError("Source not found")
        await self.db.delete(source)
        await self.db.commit()

    async def get_by_details(self, details: str):
        details = details.strip()
        result = await self.db.execute(
            select(TransactionSource).where(TransactionSource.name == details)
        )
        return result.scalars().first()
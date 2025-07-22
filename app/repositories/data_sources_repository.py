from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, exists
from app.models.data_sources import DataSource
from app.schemas.data_sources import DataSourceCreate, DataSourceUpdate

class DataSourceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(DataSource))
        return result.scalars().all()
    
    async def get_all_short(self):
        query = select(DataSource.id, DataSource.name).distinct()
        result = await self.db.execute(query)
        return [{"id": row.id, "name": row.name} for row in result]

    async def create(self, data: DataSourceCreate):
        new_data_source = DataSource(**data.dict())
        self.db.add(new_data_source)
        await self.db.commit()
        await self.db.refresh(new_data_source)
        return new_data_source

    async def update(self, data_source_id: int, data: DataSourceUpdate):
        result = await self.db.execute(select(DataSource).where(DataSource.id == data_source_id))
        existing = result.scalars().first()
        if not existing:
            raise ValueError("Data source not found")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        self.db.add(existing)
        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete(self, data_source_id: int):
        category = await self.db.get(DataSource, data_source_id)
        if not category:
            raise ValueError("DataSource not found")
        await self.db.delete(category)
        await self.db.commit()

    async def exists_by_name(self, name: str):
        result = await self.db.execute(select(exists().where(DataSource.name == name)))
        return result.scalar()

    async def exists_by_name_and_not_id(self, name: str, data_source_id: int):
        result = await self.db.execute(
            select(exists().where(DataSource.name == name, DataSource.id != data_source_id))
        )
        return result.scalar()

    async def is_used_as_foreign_key(self, data_source_id: int):
        return False
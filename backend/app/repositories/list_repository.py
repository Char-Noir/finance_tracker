from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from fastapi import Depends
from app.models.list import List
from app.database import SessionLocal
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

class ListRepository:

    async def get_all(self, page: int = 1, size: int = 10, sort_by: str = "created_at", order: str = "desc"):
        async with get_session_local() as db:
            total_query = select(func.count()).select_from(List)
            total_result = await db.execute(total_query)
            total_count = total_result.scalar()
        
            query = select(List)
            query = query.order_by(getattr(List, sort_by).desc() if order == "desc" else getattr(List, sort_by).asc())
            query = query.offset((page - 1) * size).limit(size)
            result = await db.execute(query)
            lists = result.scalars().all()
        
            return {
                "lists": [{"id": l.id, "name": l.name, "author": l.author, "created_at": l.created_at, "updated_at": l.updated_at} for l in lists],
                "total_pages": (total_count // size) + (1 if total_count % size else 0),
                "current_page": page
            }

    async def get_by_id(self, list_id: int):
        async with get_session_local() as db:
            query = select(List).where(List.id == list_id)
            result = await db.execute(query)
            list_item = result.scalars().first()
            return {"id": list_item.id, "name": list_item.name, "author": list_item.author, "created_at": list_item.created_at, "updated_at": list_item.updated_at} if list_item else None

    async def create(self, name: str, author: str):
        async with get_session_local() as db:
            new_list = List(name=name, author=author)
            db.add(new_list)
            await db.commit()
            await db.refresh(new_list)
            return {"id": new_list.id, "name": new_list.name, "author": new_list.author, "created_at": new_list.created_at, "updated_at": new_list.updated_at}

    async def update(self, list_id: int, name: str):
        async with get_session_local() as db:
            list_item = await self.get_by_id(list_id)
            if list_item:
                list_item_obj = await db.get(List, list_id)
                list_item_obj.name = name
                await db.commit()
                await db.refresh(list_item_obj)
                return {"id": list_item_obj.id, "name": list_item_obj.name, "author": list_item_obj.author, "created_at": list_item_obj.created_at, "updated_at": list_item_obj.updated_at}
            return None

    async def delete(self, list_id: int):
        async with get_session_local() as db:
            list_item = await db.get(List, list_id)
            if list_item:
                await db.delete(list_item)
                await db.commit()
                return {"message": "List deleted successfully"}
            return None

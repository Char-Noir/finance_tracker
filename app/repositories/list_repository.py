from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.models.list import List

class ListRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, page: int = 1, size: int = 10, sort_by: str = "created_at", order: str = "desc"):
        total_query = select(func.count()).select_from(List)
        total_result = await self.db.execute(total_query)
        total_count = total_result.scalar()
    
        query = select(List)
        query = query.order_by(getattr(List, sort_by).desc() if order == "desc" else getattr(List, sort_by).asc())
        query = query.offset((page - 1) * size).limit(size)
        result = await self.db.execute(query)
        lists = result.scalars().all()
    
        return {
            "lists": [{"id": l.id, "name": l.name, "author": l.author, "created_at": l.created_at, "updated_at": l.updated_at} for l in lists],
            "total_pages": (total_count // size) + (1 if total_count % size else 0),
            "current_page": page
        }

    async def get_by_id(self, list_id: int):
        query = select(List).where(List.id == list_id)
        result = await self.db.execute(query)
        list_item = result.scalars().first()
        return {"id": list_item.id, "name": list_item.name, "author": list_item.author, "created_at": list_item.created_at, "updated_at": list_item.updated_at} if list_item else None

    async def create(self, name: str, author: str):
        new_list = List(name=name, author=author)
        self.db.add(new_list)
        await self.db.commit()
        await self.db.refresh(new_list)
        return {"id": new_list.id, "name": new_list.name, "author": new_list.author, "created_at": new_list.created_at, "updated_at": new_list.updated_at}

    async def update(self, list_id: int, name: str):
        list_item = await self.db.get(List, list_id)
        if list_item:
            list_item.name = name
            await self.db.commit()
            await self.db.refresh(list_item)
            return {"id": list_item.id, "name": list_item.name, "author": list_item.author, "created_at": list_item.created_at, "updated_at": list_item.updated_at}
        raise ValueError("List not found")

    async def delete(self, list_id: int):
        list_item = await self.db.get(List, list_id)
        if list_item:
            await self.db.delete(list_item)
            await self.db.commit()
            return {"message": "List deleted successfully"}
        raise ValueError("List not found")
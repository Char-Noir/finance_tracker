from app.repositories.list_repository import ListRepository
from app.database import SessionLocal
from app.services.data_sources_service import ServiceException
from app.schemas.list import ListSchema

class ListService:
    async def _create_repository(self):
        db = SessionLocal()
        return ListRepository(db), db

    async def get_all(self, page: int, size: int, sort_by: str, order: str):
        repository, db = await self._create_repository()
        async with db:
            # This method returns a dict which is already JSON serializable and used by the template.
            return await repository.get_all(page, size, sort_by, order)

    async def get_by_id(self, list_id: int):
        repository, db = await self._create_repository()
        async with db:
            # This method returns a dict which is already JSON serializable.
            return await repository.get_by_id(list_id)

    async def create(self, name: str, author: str):
        repository, db = await self._create_repository()
        async with db:
            db_object = await repository.create(name, author)
            # The repository create method returns a dict, let's assume it contains the full object data
            # To be safe, let's fetch the object to convert to a schema
            new_list = await repository.get_by_id(db_object['id'])
            return new_list # It already returns a dict, which is fine.

    async def update(self, list_id: int, name: str):
        repository, db = await self._create_repository()
        async with db:
            try:
                # This method returns a dict which is already JSON serializable.
                return await repository.update(list_id, name)
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

    async def delete(self, list_id: int):
        repository, db = await self._create_repository()
        async with db:
            try:
                await repository.delete(list_id)
                return None
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

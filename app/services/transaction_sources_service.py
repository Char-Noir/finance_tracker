from app.repositories.transaction_sources_repository import TransactionSourceRepository
from app.schemas.transaction_sources import TransactionSourceCreate, TransactionSourceUpdate, TransactionSourceSchema
from app.database import SessionLocal
from app.services.data_sources_service import ServiceException

class TransactionSourceService:
    async def _create_repository(self):
        db = SessionLocal()
        return TransactionSourceRepository(db), db

    async def get_all(self, uncategorized: bool = False, sort_by: str = 'id', sort_order: str = 'asc'):
        repository, db = await self._create_repository()
        async with db:
            return await repository.get_all(uncategorized, sort_by, sort_order)
    
    async def get_all_sh(self):
        repository, db = await self._create_repository()
        async with db:
            return await repository.get_all_short()

    async def create(self, data: TransactionSourceCreate):
        repository, db = await self._create_repository()
        async with db:
            db_object = await repository.create(data)
            return TransactionSourceSchema.from_orm(db_object)

    async def update(self, source_id: int, data: TransactionSourceUpdate):
        repository, db = await self._create_repository()
        async with db:
            try:
                db_object = await repository.update(source_id, data)
                return TransactionSourceSchema.from_orm(db_object)
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

    async def delete(self, source_id: int):
        repository, db = await self._create_repository()
        async with db:
            try:
                await repository.delete(source_id)
                return None
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

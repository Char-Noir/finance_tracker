from app.repositories.transaction_source_category_repository import TransactionSourceCategoryRepository
from app.schemas.transaction_source_category import TransactionSourceCategoryCreate, TransactionSourceCategoryUpdate, TransactionSourceCategorySchema
from app.database import SessionLocal
from app.services.data_sources_service import ServiceException

class TransactionSourceCategoryService:
    async def _create_repository(self):
        db = SessionLocal()
        return TransactionSourceCategoryRepository(db), db

    async def get_all(self):
        repository, db = await self._create_repository()
        async with db:
            db_objects = await repository.get_all()
            return [TransactionSourceCategorySchema.from_orm(obj) for obj in db_objects]
    
    async def get_all_sh(self):
        repository, db = await self._create_repository()
        async with db:
            return await repository.get_all_short()

    async def create(self, data: TransactionSourceCategoryCreate):
        repository, db = await self._create_repository()
        async with db:
            db_object = await repository.create(data)
            return TransactionSourceCategorySchema.from_orm(db_object)

    async def update(self, category_id: int, data: TransactionSourceCategoryUpdate):
        repository, db = await self._create_repository()
        async with db:
            try:
                db_object = await repository.update(category_id, data)
                return TransactionSourceCategorySchema.from_orm(db_object)
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

    async def delete(self, category_id: int):
        repository, db = await self._create_repository()
        async with db:
            try:
                await repository.delete(category_id)
                return None
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)
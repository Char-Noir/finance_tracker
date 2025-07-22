from app.repositories.data_sources_repository import DataSourceRepository
from app.schemas.data_sources import DataSourceCreate, DataSourceUpdate, DataSourceSchema
from app.database import SessionLocal

class ServiceException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

class DataSourceService:
    async def _create_repository(self):
        db = SessionLocal()
        return DataSourceRepository(db), db

    async def get_all_data_sources(self):
        repository, db = await self._create_repository()
        async with db:
            db_objects = await repository.get_all()
            return [DataSourceSchema.from_orm(obj) for obj in db_objects]

    async def get_all_data_sources_sh(self):
        repository, db = await self._create_repository()
        async with db:
            return await repository.get_all_short()

    async def create_data_source(self, data: DataSourceCreate):
        if len(data.name) < 3:
            raise ServiceException(message="Name must be at least 3 characters long", status_code=400)
        repository, db = await self._create_repository()
        async with db:
            if await repository.exists_by_name(data.name):
                raise ServiceException(message="Data source with this name already exists", status_code=400)
            db_object = await repository.create(data)
            return DataSourceSchema.from_orm(db_object)

    async def update_data_source(self, data_source_id: int, data: DataSourceUpdate):
        if len(data.name) < 3:
            raise ServiceException(message="Name must be at least 3 characters long", status_code=400)
        repository, db = await self._create_repository()
        async with db:
            if await repository.exists_by_name_and_not_id(data.name, data_source_id):
                raise ServiceException(message="Data source with this name already exists", status_code=400)
            try:
                db_object = await repository.update(data_source_id, data)
                return DataSourceSchema.from_orm(db_object)
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)

    async def delete_data_source(self, data_source_id: int):
        repository, db = await self._create_repository()
        async with db:
            if await repository.is_used_as_foreign_key(data_source_id):
                raise ServiceException(message="Data source is used as a foreign key and cannot be deleted", status_code=400)
            try:
                await repository.delete(data_source_id)
                return None # No content to return on successful deletion
            except ValueError as e:
                raise ServiceException(message=str(e), status_code=404)
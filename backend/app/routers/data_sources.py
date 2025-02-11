from fastapi import APIRouter, HTTPException, Depends
from app.services.data_sources_service import DataSourceService
from app.schemas.data_sources import DataSourceCreate, DataSourceUpdate

router = APIRouter(
    prefix="/data-sources",
    tags=["Data Sources"]
)

@router.get("/")
async def get_all_data_sources(service: DataSourceService = Depends(DataSourceService)):
    return await service.get_all_data_sources()

@router.get("/sh")
async def get_all_data_sources(service: DataSourceService = Depends(DataSourceService)):
    return await service.get_all_data_sources_sh()

@router.post("/")
async def create_data_source(data: DataSourceCreate, service: DataSourceService = Depends(DataSourceService)):
    return await service.create_data_source(data)

@router.put("/{data_source_id}")
async def update_data_source(data_source_id: int, data: DataSourceUpdate, service: DataSourceService = Depends(DataSourceService)):
    return await service.update_data_source(data_source_id, data)

@router.delete("/{data_source_id}")
async def delete_data_source(data_source_id: int, service: DataSourceService = Depends(DataSourceService)):
    return await service.delete_data_source(data_source_id)

from fastapi import APIRouter, HTTPException, Depends
from app.services.transaction_sources_service import *
from app.schemas.transaction_sources import *

router = APIRouter(prefix="/transaction-sources", tags=["Transaction Sources"])

@router.get("/")
async def get_all(service: TransactionSourceService = Depends(TransactionSourceService)):
    return await service.get_all()

@router.get("/sh")
async def get_all(service: TransactionSourceService = Depends(TransactionSourceService)):
    return await service.get_all_sh()

@router.post("/")
async def create(data: TransactionSourceCreate, service: TransactionSourceService = Depends(TransactionSourceService)):
    return await service.create(data)

@router.put("/{source_id}")
async def update(source_id: int, data: TransactionSourceUpdate, service: TransactionSourceService = Depends(TransactionSourceService)):
    return await service.update(source_id, data)

@router.delete("/{source_id}")
async def delete(source_id: int, service: TransactionSourceService = Depends(TransactionSourceService)):
    return await service.delete(source_id)

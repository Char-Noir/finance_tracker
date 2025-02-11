from fastapi import APIRouter, HTTPException, Depends
from app.services.transaction_source_category_service import TransactionSourceCategoryService
from app.schemas.transaction_source_category import TransactionSourceCategoryCreate, TransactionSourceCategoryUpdate

router = APIRouter(prefix="/transaction-source-categories", tags=["Transaction Source Categories"])

@router.get("/")
async def get_all(service: TransactionSourceCategoryService = Depends(TransactionSourceCategoryService)):
    return await service.get_all()

@router.get("/sh")
async def get_all(service: TransactionSourceCategoryService = Depends(TransactionSourceCategoryService)):
    return await service.get_all_sh()

@router.post("/")
async def create(data: TransactionSourceCategoryCreate, service: TransactionSourceCategoryService = Depends(TransactionSourceCategoryService)):
    return await service.create(data)

@router.put("/{category_id}")
async def update(category_id: int, data: TransactionSourceCategoryUpdate, service: TransactionSourceCategoryService = Depends(TransactionSourceCategoryService)):
    return await service.update(category_id, data)

@router.delete("/{category_id}")
async def delete(category_id: int, service: TransactionSourceCategoryService = Depends(TransactionSourceCategoryService)):
    return await service.delete(category_id)

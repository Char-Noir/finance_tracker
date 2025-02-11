from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends
from app.services.upload_transactions_service import UploadTransactionsService
import pandas as pd

router = APIRouter(prefix="/upload-transactions", tags=["Upload Transactions"])

@router.post("/")
async def upload_transactions(
    data_source_id: int = Form(...),
    file: UploadFile = Form(...),
    service: UploadTransactionsService = Depends()
):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Файл повинен бути csv.")

    try:
        # Читаємо CSV у DataFrame
        df = pd.read_csv(file.file, delimiter=",",)
        await service.process_csv(data_source_id, df)
        return {"message": "Завантажено успішно."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

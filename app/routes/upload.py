from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.upload_service import process_csv
from app.schemas import UploadResponse

router = APIRouter()


@router.post("/upload-grades", response_model=UploadResponse)
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "")
    try:
        content = await file.read()
        records_loaded, students = await process_csv(content)
        return UploadResponse(status="ok", records_loaded=records_loaded, students=students)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
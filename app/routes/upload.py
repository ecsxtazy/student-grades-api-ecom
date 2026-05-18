from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import asyncpg
from app.services.upload_service import process_upload
from app.repositories.student_repository import StudentRepository
from app.schemas import UploadResponse
from app.database import db_pool


async def get_repo() -> StudentRepository:
    pool = await db_pool.get_pool()
    return StudentRepository(pool)


router = APIRouter()


@router.post("/upload-grades", response_model=UploadResponse)
async def upload_grades(
    file: UploadFile = File(...),
    repo: StudentRepository = Depends(get_repo)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only csv files allowed")
    try:
        content = await file.read()
        records_loaded, students_count = await process_upload(repo, content)
        return UploadResponse(status="ok", records_loaded=records_loaded, students=students_count)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
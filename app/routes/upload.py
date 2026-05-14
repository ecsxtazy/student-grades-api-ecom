from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import asyncpg
from app.services.upload_service import parse_csv
from app.repositories.student_repository import insert_students, insert_grades
from app.schemas import UploadResponse
from app.database import db_pool


async def get_pool() -> asyncpg.Pool:
    return await db_pool.get_pool()


router = APIRouter()


@router.post("/upload-grades", response_model=UploadResponse)
async def upload_grades(
    file: UploadFile = File(...),
    pool: asyncpg.Pool = Depends(get_pool)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only csv files allowed")
    try:
        content = await file.read()
        student_grades, records_loaded, students_count = await parse_csv(content)
        student_names = list(student_grades.keys())
        name_to_id = await insert_students(pool, student_names)
        grade_records = []
        for name, grades in student_grades.items():
            student_id = name_to_id[name]
            for grade in grades:
                grade_records.append((student_id, grade))
        await insert_grades(pool, grade_records)
        
        return UploadResponse(status="ok", records_loaded=records_loaded, students=students_count)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
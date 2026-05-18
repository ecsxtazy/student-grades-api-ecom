import asyncpg
from fastapi import APIRouter, Depends
from app.repositories.student_repository import StudentRepository
from app.schemas import StudentTwosCount
from app.database import db_pool

router = APIRouter()
async def get_repo() -> StudentRepository:
    pool = await db_pool.get_pool()
    return StudentRepository(pool)




@router.get("/students/more-than-3-twos", response_model=list[StudentTwosCount])
async def more_than_3_twos(repo: StudentRepository = Depends(get_repo)):
    return await repo.get_more_than_3_twos()


@router.get("/students/less-than-5-twos", response_model=list[StudentTwosCount])
async def less_than_5_twos(repo: StudentRepository = Depends(get_repo)):
    return await repo.get_less_than_5_twos()
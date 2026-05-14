import asyncpg
from fastapi import APIRouter, Depends
from app.repositories.student_repository import get_more_than_3_twos, get_less_than_5_twos
from app.schemas import StudentTwosCount
from app.database import db_pool

router = APIRouter()
async def get_pool() -> asyncpg.Pool:
    return await db_pool.get_pool()


@router.get("/students/more-than-3-twos", response_model=list[StudentTwosCount])
async def more_than_3_twos(pool: asyncpg.Pool = Depends(get_pool)):
    return await get_more_than_3_twos(pool)


@router.get("/students/less-than-5-twos", response_model=list[StudentTwosCount])
async def less_than_5_twos(pool: asyncpg.Pool = Depends(get_pool)):
    return await get_less_than_5_twos(pool)
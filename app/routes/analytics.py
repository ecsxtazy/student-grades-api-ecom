from fastapi import APIRouter
from app.repositories.student_repository import get_more_than_3_twos, get_less_than_5_twos
from app.schemas import StudentTwosCount

router = APIRouter()


@router.get("/students/more-than-3-twos", response_model=list[StudentTwosCount])
async def more_than_3_twos():
    return await get_more_than_3_twos()


@router.get("/students/less-than-5-twos", response_model=list[StudentTwosCount])
async def less_than_5_twos():
    return await get_less_than_5_twos()
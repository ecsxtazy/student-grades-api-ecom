from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from app.database import db_pool
from app.routes import upload, analytics
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/grades_db")
    await db_pool.init(dsn)
    yield
    await db_pool.close()
app = FastAPI(
    title="Student Grades Service",
    lifespan=lifespan,
    version="1.0.0"
)

app.include_router(upload.router)
app.include_router(analytics.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ecom",status_code=status.HTTP_418_IM_A_TEAPOT)
async def teapot():
    return {"message": "I'm a teapot"}
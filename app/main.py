from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db, close_db
from app.routes import upload, analytics
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/grades_db")
    await init_db(dsn)
    yield
    await close_db()
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

@app.get("/ecom")
async def teapot():
    return {"message": "I'm a teapot"}, 418
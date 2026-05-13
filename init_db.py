import asyncio
import asyncpg
import os

async def init():
    dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/grades_db")    
    conn = await asyncpg.connect(dsn)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            grade INTEGER NOT NULL CHECK (grade >= 2 AND grade <= 5)
        );
    """)    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(init())
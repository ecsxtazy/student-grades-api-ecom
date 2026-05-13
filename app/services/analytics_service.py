from app.database import get_db

async def get_more_than_3_twos():
    pool = await get_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT s.full_name, COUNT(g.id) as count_twos
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.grade = 2
            GROUP BY s.id, s.full_name
            HAVING COUNT(g.id) > 3
            ORDER BY s.full_name
        """)
    return [{"full_name": row["full_name"], "count_twos": row["count_twos"]} for row in rows]
async def get_less_than_5_twos():
    pool = await get_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT s.full_name, COUNT(g.id) as count_twos
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.grade = 2
            GROUP BY s.id, s.full_name
            HAVING COUNT(g.id) < 5
            ORDER BY s.full_name
        """)
from typing import Dict, List, Tuple
import asyncpg


async def insert_students(pool: asyncpg.Pool, student_names: List[str]) -> Dict[str, int]:
    async with pool.acquire() as conn:
        existing = await conn.fetch(
            "SELECT id, full_name FROM students WHERE full_name = ANY($1)",
            student_names
        )
        name_to_id = {row['full_name']: row['id'] for row in existing}
        new_names = [name for name in student_names if name not in name_to_id]
        for name in new_names:
            row = await conn.fetchrow(
                "INSERT INTO students (full_name) VALUES ($1) RETURNING id",
                name
            )
            name_to_id[name] = row['id']
        return name_to_id


async def insert_grades(pool: asyncpg.Pool, grade_records: List[Tuple[int, int]]) -> None:
    async with pool.acquire() as conn:
        await conn.executemany(
            "INSERT INTO grades (student_id, grade) VALUES ($1, $2)",
            grade_records
        )


async def get_more_than_3_twos(pool: asyncpg.Pool) -> List[Dict]:
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


async def get_more_than_5_twos(pool: asyncpg.Pool) -> List[Dict]:
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
    return [{"full_name": row["full_name"], "count_twos": row["count_twos"]} for row in rows]
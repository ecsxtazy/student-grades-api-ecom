import asyncpg

_pool = None

async def init_db(dsn: str):
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn, min_size=1, max_size=10)

async def get_db():
    return _pool

async def close_db():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
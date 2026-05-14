import asyncpg


class DatabasePool:
    def __init__(self):
        self._pool = None

    async def init(self, dsn: str) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(dsn, min_size=1, max_size=10)

    async def get_pool(self) -> asyncpg.Pool:
        return self._pool

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None


db_pool = DatabasePool()
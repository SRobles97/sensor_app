import os
import dotenv
import asyncpg
from typing import Optional

dotenv.load_dotenv()

conn_pool: Optional[asyncpg.Pool] = None

async def connect_db():
    global conn_pool
    conn_pool = await asyncpg.create_pool(
        dsn=os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=5,
    )

async def disconnect_db():
    global conn_pool
    if conn_pool:
        await conn_pool.close()

async def get_pool() -> asyncpg.Pool:
    if conn_pool is None:
        raise RuntimeError("DB pool not initialized")
    return conn_pool
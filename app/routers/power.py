from fastapi import APIRouter, Depends, Query
from datetime import datetime
from database import get_pool
import asyncpg

router = APIRouter(prefix="/api/power", tags=["Consultas Power"])


@router.get("/by-time-range")
async def get_by_time_range(
    device: str, start: datetime, end: datetime, db: asyncpg.Pool = Depends(get_pool)
):
    async with db.acquire() as conn:
        result = await conn.fetch(
            """
            SELECT * FROM power_measurements
            WHERE device = $1
              AND timestamp >= $2
              AND timestamp <= $3
            ORDER BY timestamp DESC;
            """,
            device,
            start,
            end,
        )
        return [dict(r) for r in result]

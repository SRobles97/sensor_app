from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime
from app.database.database import get_pool
import asyncpg

router = APIRouter(prefix="/api/power", tags=["Consultas Power"])


@router.get("/by-time-range")
async def get_by_time_range(
    device: str,
    start_date: str = Query(..., description="Formato: dd-mm-yyyy"),
    start_time: str = Query(..., description="Formato: HH:MM"),
    end_date: str = Query(..., description="Formato: dd-mm-yyyy"),
    end_time: str = Query(..., description="Formato: HH:MM"),
    limit: int = Query(500, ge=1, le=10000),
    db: asyncpg.Pool = Depends(get_pool)
):
    try:
        start_dt = datetime.strptime(f"{start_date} {start_time}", "%d-%m-%Y %H:%M")
        end_dt = datetime.strptime(f"{end_date} {end_time}", "%d-%m-%Y %H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato inválido. Usa fechas como dd-mm-yyyy y horas como HH:MM",
        )

    if start_dt > end_dt:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser anterior a la fecha de término")

    async with db.acquire() as conn:
        result = await conn.fetch(
            """
            SELECT *
            FROM power_measurements
            WHERE device = $1
              AND timestamp >= $2
              AND timestamp <= $3
            ORDER BY timestamp DESC
            LIMIT $4;
            """,
            device,
            start_dt,
            end_dt,
            limit,
        )
        return [dict(r) for r in result]
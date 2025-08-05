from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.database.database import get_pool
from app.models.discrete_sensor_data import SensorData
from app.utils import parse_and_validate_time_range, PaginatedResponse, build_optimized_query, build_count_query
import asyncpg

router = APIRouter(prefix="/api/discrete", tags=["Consultas Discrete"])


@router.get("/by-time-range", response_model=PaginatedResponse)
async def get_by_time_range(
    device: str,
    start_date: str = Query(..., description="Formato: dd-mm-yyyy"),
    start_time: str = Query(..., description="Formato: HH:MM"),
    end_date: str = Query(..., description="Formato: dd-mm-yyyy"),
    end_time: str = Query(..., description="Formato: HH:MM"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(500, ge=1, le=1000, description="Registros por página"),
    cursor: Optional[str] = Query(None, description="Cursor para paginación optimizada"),
    db: asyncpg.Pool = Depends(get_pool),
):
    start_dt, end_dt = parse_and_validate_time_range(start_date, start_time, end_date, end_time)

    async with db.acquire() as conn:
        # Get optimized query
        query, params = build_optimized_query(
            "discrete_measurements", device, start_dt, end_dt, page, page_size, cursor
        )
        
        # Execute data query
        result = await conn.fetch(query, *params)
        data = [dict(r) for r in result]
        
        # Get total count for pagination info
        count_query, count_params = build_count_query("discrete_measurements", device, start_dt, end_dt)
        total_count_result = await conn.fetchval(count_query, *count_params)
        total_count = total_count_result or 0
        
        # Calculate pagination metadata
        has_next = len(data) == page_size and ((page * page_size) < total_count)
        has_previous = page > 1
        next_cursor = data[-1]["timestamp"].isoformat() if data and has_next else None
        
        return PaginatedResponse(
            data=data,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_previous=has_previous,
            next_cursor=next_cursor
        )


@router.get("/by-time-range/simple", response_model=List[SensorData])
async def get_by_time_range_simple(
    device: str,
    start_date: str = Query(..., description="Formato: dd-mm-yyyy"),
    start_time: str = Query(..., description="Formato: HH:MM"),
    end_date: str = Query(..., description="Formato: dd-mm-yyyy"),
    end_time: str = Query(..., description="Formato: HH:MM"),
    limit: int = Query(500, ge=1, le=1000),
    db: asyncpg.Pool = Depends(get_pool),
):
    """Endpoint simple sin paginación para compatibilidad hacia atrás."""
    start_dt, end_dt = parse_and_validate_time_range(start_date, start_time, end_date, end_time)

    async with db.acquire() as conn:
        query, params = build_optimized_query(
            "discrete_measurements", device, start_dt, end_dt, 1, limit
        )
        result = await conn.fetch(query, *params)
        return [SensorData(**dict(r)) for r in result]

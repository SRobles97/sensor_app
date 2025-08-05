from datetime import datetime
from fastapi import HTTPException
from typing import Tuple, Optional, Dict, Any, List
from pydantic import BaseModel


def parse_and_validate_time_range(
    start_date: str, start_time: str, end_date: str, end_time: str
) -> Tuple[datetime, datetime]:
    """
    Parsea y valida un rango de tiempo desde strings de fecha y hora.
    
    Args:
        start_date: Fecha de inicio en formato dd-mm-yyyy
        start_time: Hora de inicio en formato HH:MM
        end_date: Fecha de fin en formato dd-mm-yyyy
        end_time: Hora de fin en formato HH:MM
    
    Returns:
        Tuple con datetime de inicio y fin
        
    Raises:
        HTTPException: Si el formato es inválido o el rango es incorrecto
    """
    try:
        start_dt = datetime.strptime(f"{start_date} {start_time}", "%d-%m-%Y %H:%M")
        end_dt = datetime.strptime(f"{end_date} {end_time}", "%d-%m-%Y %H:%M")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato inválido. Usa fechas como dd-mm-yyyy y horas como HH:MM",
        )

    if start_dt > end_dt:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio debe ser anterior a la fecha de término"
        )

    return start_dt, end_dt


class PaginatedResponse(BaseModel):
    """Respuesta paginada estándar para consultas de sensores."""
    data: List[Dict[str, Any]]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool
    next_cursor: Optional[str] = None


def build_optimized_query(
    table_name: str,
    device: str,
    start_dt: datetime,
    end_dt: datetime,
    page: int = 1,
    page_size: int = 500,
    cursor: Optional[str] = None
) -> Tuple[str, List[Any]]:
    """
    Construye una consulta optimizada con paginación por cursor y offset.
    
    Args:
        table_name: Nombre de la tabla a consultar
        device: Dispositivo a filtrar
        start_dt: Fecha/hora de inicio
        end_dt: Fecha/hora de fin
        page: Número de página (1-indexed)
        page_size: Tamaño de página
        cursor: Cursor para paginación basada en timestamp
    
    Returns:
        Tuple con la query SQL y lista de parámetros
    """
    offset = (page - 1) * page_size
    
    if cursor:
        # Cursor-based pagination for better performance on large datasets
        cursor_dt = datetime.fromisoformat(cursor)
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE device = $1
              AND timestamp >= $2
              AND timestamp <= $3
              AND timestamp < $4
            ORDER BY timestamp DESC
            LIMIT $5;
        """
        params = [device, start_dt, end_dt, cursor_dt, page_size]
    else:
        # Offset-based pagination with optimizations
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE device = $1
              AND timestamp >= $2
              AND timestamp <= $3
            ORDER BY timestamp DESC
            LIMIT $4 OFFSET $5;
        """
        params = [device, start_dt, end_dt, page_size, offset]
    
    return query, params


def build_count_query(table_name: str, device: str, start_dt: datetime, end_dt: datetime) -> Tuple[str, List[Any]]:
    """
    Construye una consulta optimizada para contar registros.
    
    Returns:
        Tuple con la query SQL y lista de parámetros
    """
    query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        WHERE device = $1
          AND timestamp >= $2
          AND timestamp <= $3;
    """
    return query, [device, start_dt, end_dt]
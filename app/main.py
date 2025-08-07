from fastapi import FastAPI
from app.database.database import connect_db, disconnect_db
from app.routers import power, discrete

app = FastAPI(title="API de Consulta de Sensores")

app.include_router(power.router)
app.include_router(discrete.router)


@app.get("/", tags=["Información del Sistema"])
async def read_root():
    """
    Información general del sistema API.

    Returns:
        dict: Información sobre versión, endpoints disponibles y estado
    """
    return {
        "version": "1.0.0",
        "description": "API para consultas de sensores y mediciones.",
        "endpoints": {
            "/api/power/by-time-range": "Consulta de datos de potencia por rango de tiempo",
            "/api/discrete/by-time-range": "Consulta de datos discretos por rango de tiempo",
            "/api/discrete/by-time-range/simple": "Consulta simple de datos discretos por rango de tiempo",
        },
        "status": "API en funcionamiento",
        "documentation": "/docs",
        "redoc": "/redoc"
    }


@app.on_event("startup")
async def startup():
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

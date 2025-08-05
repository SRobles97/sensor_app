from fastapi import FastAPI
from app.database.database import connect_db, disconnect_db
from app.routers import power, discrete

app = FastAPI(title="API de Consulta de Sensores")

app.include_router(power.router)
app.include_router(discrete.router)


@app.on_event("startup")
async def startup():
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

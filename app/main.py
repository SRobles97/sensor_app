from fastapi import FastAPI
from database import connect_db, disconnect_db
from routers import power

app = FastAPI(title="API de Consulta de Sensores")

app.include_router(power.router)


@app.on_event("startup")
async def startup():
    await connect_db()


@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

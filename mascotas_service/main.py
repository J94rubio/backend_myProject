from fastapi import FastAPI
from mascotas_service.routes.mascotas import router as mascotas_router


app = FastAPI(
    title="DatesPets Backend",
    description="API para el sistema veterinario DatesPets",
    version="1.0.0",
)


app.include_router(mascotas_router)


@app.get("/", tags=["Health"])
def inicio():

    return {
        "message": "DatesPets Backend funcionando"
    }
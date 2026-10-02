from fastapi import FastAPI

from citas_service.routes.citas import router as citas_router


app = FastAPI(
    title="DatesPets - Citas Service",
    description="Microservicio para la gestión de citas veterinarias",
    version="1.0.0",
)


app.include_router(citas_router)


@app.get("/", tags=["Health"])
def inicio():
    return {
        "message": "DatesPets Citas Service funcionando"
    }
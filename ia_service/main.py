from fastapi import FastAPI

from ia_service.routes.chat import router as chat_router


app = FastAPI(
    title="DatesPets - IA Service",
    description="Microservicio de asistente veterinario con IA",
    version="1.0.0",
)


app.include_router(chat_router)


@app.get("/", tags=["Health"])
def inicio():

    return {
        "message": "DatesPets IA Service funcionando"
    }   
from fastapi import APIRouter, HTTPException

from ia_service.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from ia_service.services.ia import (
    generar_respuesta
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat IA"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(datos: ChatRequest):

    try:

        print("\n==============================")
        print("MENSAJE RECIBIDO")
        print(datos.mensaje)
        print("==============================")

        resultado = generar_respuesta(
            mensaje=datos.mensaje,
            previous_interaction_id=(
                datos.previous_interaction_id
            )
        )

        print("\n==============================")
        print("RESPUESTA GENERADA")
        print(resultado)
        print("==============================")

        return resultado

    except Exception as e:

        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("ERROR EN CHAT IA")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(type(e).__name__)
        print(str(e))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

        mensaje_error = str(e)

        if "429" in mensaje_error or "RESOURCE_EXHAUSTED" in mensaje_error:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Se alcanzó el límite de uso de la IA. "
                    "Intenta de nuevo en unos minutos."
                )
            )

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {mensaje_error}"
        )
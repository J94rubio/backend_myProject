from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    mensaje: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    previous_interaction_id: str | None = None


class ChatResponse(BaseModel):

    respuesta: str

    interaction_id: str
from datetime import date

from pydantic import BaseModel, Field


class CitaBase(BaseModel):

    mascota_id: int = Field(
        ...,
        gt=0
    )

    fecha: date

    motivo: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    estado: str = Field(
        default="Pendiente",
        pattern="^(Pendiente|Confirmada|Completada|Cancelada)$"
    )


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):

    mascota_id: int | None = Field(
        default=None,
        gt=0
    )

    fecha: date | None = None

    motivo: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    estado: str | None = Field(
        default=None,
        pattern="^(Pendiente|Confirmada|Completada|Cancelada)$"
    )


class CitaResponse(CitaBase):

    id: int
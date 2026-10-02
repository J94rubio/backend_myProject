from pydantic import BaseModel, Field


class MascotaBase(BaseModel):

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    especie: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    raza: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    edad: int = Field(
        ...,
        ge=0
    )

    propietario: str = Field(
        ...,
        min_length=2,
        max_length=150
    )


class MascotaCreate(MascotaBase):
    pass


class MascotaUpdate(BaseModel):

    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    especie: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    raza: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    edad: int | None = Field(
        default=None,
        ge=0
    )

    propietario: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )


class MascotaResponse(MascotaBase):

    id: int
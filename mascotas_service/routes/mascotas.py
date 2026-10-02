from fastapi import APIRouter, HTTPException, status

from mascotas_service.database import supabase
from mascotas_service.schemas.mascota import (
    MascotaCreate,
    MascotaResponse,
    MascotaUpdate
)


router = APIRouter(
    prefix="/api/mascotas",
    tags=["Mascotas"]
)


# ==========================================
# GET - LISTAR MASCOTAS
# ==========================================

@router.get(
    "/",
    response_model=list[MascotaResponse]
)
def listar_mascotas():

    response = (
        supabase
        .table("mascotas")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


# ==========================================
# GET - OBTENER MASCOTA POR ID
# ==========================================

@router.get(
    "/{mascota_id}",
    response_model=MascotaResponse
)
def obtener_mascota(mascota_id: int):

    response = (
        supabase
        .table("mascotas")
        .select("*")
        .eq("id", mascota_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada"
        )

    return response.data[0]


# ==========================================
# POST - CREAR MASCOTA
# ==========================================

@router.post(
    "/",
    response_model=MascotaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_mascota(datos: MascotaCreate):

    response = (
        supabase
        .table("mascotas")
        .insert(
            datos.model_dump()
        )
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fue posible crear la mascota"
        )

    return response.data[0]


# ==========================================
# PUT - ACTUALIZAR MASCOTA
# ==========================================

@router.put(
    "/{mascota_id}",
    response_model=MascotaResponse
)
def actualizar_mascota(
    mascota_id: int,
    datos: MascotaUpdate
):

    cambios = datos.model_dump(
        exclude_unset=True
    )

    if not cambios:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron datos para actualizar"
        )

    response = (
        supabase
        .table("mascotas")
        .update(cambios)
        .eq("id", mascota_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada"
        )

    return response.data[0]


# ==========================================
# DELETE - ELIMINAR MASCOTA
# ==========================================

@router.delete(
    "/{mascota_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_mascota(mascota_id: int):

    response = (
        supabase
        .table("mascotas")
        .delete()
        .eq("id", mascota_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada"
        )
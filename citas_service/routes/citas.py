from fastapi import APIRouter, HTTPException, status

from citas_service.database import supabase

from citas_service.schemas.cita import (
    CitaCreate,
    CitaResponse,
    CitaUpdate
)


router = APIRouter(
    prefix="/api/citas",
    tags=["Citas"]
)


# ==========================================
# FUNCIÓN AUXILIAR
# ==========================================

def verificar_mascota(mascota_id: int):

    response = (
        supabase
        .table("mascotas")
        .select("id")
        .eq("id", mascota_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La mascota indicada no existe"
        )


# ==========================================
# GET - LISTAR TODAS LAS CITAS
# ==========================================

@router.get(
    "/",
    response_model=list[CitaResponse]
)
def listar_citas():

    response = (
        supabase
        .table("citas")
        .select("*")
        .order("id")
        .execute()
    )

    return response.data


# ==========================================
# GET - OBTENER CITA POR ID
# ==========================================

@router.get(
    "/{cita_id}",
    response_model=CitaResponse
)
def obtener_cita(cita_id: int):

    response = (
        supabase
        .table("citas")
        .select("*")
        .eq("id", cita_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )

    return response.data[0]


# ==========================================
# GET - CITAS DE UNA MASCOTA
# ==========================================

@router.get(
    "/mascota/{mascota_id}",
    response_model=list[CitaResponse]
)
def listar_citas_mascota(mascota_id: int):

    verificar_mascota(mascota_id)

    response = (
        supabase
        .table("citas")
        .select("*")
        .eq("mascota_id", mascota_id)
        .order("fecha")
        .execute()
    )

    return response.data


# ==========================================
# POST - CREAR CITA
# ==========================================

@router.post(
    "/",
    response_model=CitaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_cita(datos: CitaCreate):

    # Verificar que la mascota exista
    verificar_mascota(datos.mascota_id)

    response = (
        supabase
        .table("citas")
        .insert(
            datos.model_dump(mode="json")
        )
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fue posible crear la cita"
        )

    return response.data[0]


# ==========================================
# PUT - ACTUALIZAR CITA
# ==========================================

@router.put(
    "/{cita_id}",
    response_model=CitaResponse
)
def actualizar_cita(
    cita_id: int,
    datos: CitaUpdate
):

    # Verificar que la cita exista
    cita_response = (
        supabase
        .table("citas")
        .select("*")
        .eq("id", cita_id)
        .execute()
    )

    if not cita_response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )

    cambios = datos.model_dump(
        exclude_unset=True,
        mode="json"
    )

    if not cambios:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron datos para actualizar"
        )

    # Si se está modificando mascota_id,
    # verificar que la nueva mascota exista
    if "mascota_id" in cambios:

        verificar_mascota(
            cambios["mascota_id"]
        )

    response = (
        supabase
        .table("citas")
        .update(cambios)
        .eq("id", cita_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fue posible actualizar la cita"
        )

    return response.data[0]


# ==========================================
# DELETE - ELIMINAR CITA
# ==========================================

@router.delete(
    "/{cita_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_cita(cita_id: int):

    response = (
        supabase
        .table("citas")
        .delete()
        .eq("id", cita_id)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
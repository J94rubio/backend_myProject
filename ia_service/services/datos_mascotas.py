import os

import requests


MASCOTAS_URL = os.getenv(
    "MASCOTAS_SERVICE_URL",
    "http://127.0.0.1:8001/api/mascotas"
).rstrip("/")

CITAS_URL = os.getenv(
    "CITAS_SERVICE_URL",
    "http://127.0.0.1:8002/api/citas"
).rstrip("/")


def buscar_mascota(nombre: str):

    response = requests.get(
        f"{MASCOTAS_URL}/"
    )

    response.raise_for_status()

    mascotas = response.json()

    nombre_busqueda = nombre.strip().lower()

    resultados = [
        mascota
        for mascota in mascotas
        if nombre_busqueda in mascota["nombre"].strip().lower()
    ]

    return {
        "encontrada": len(resultados) > 0,
        "cantidad": len(resultados),
        "mascotas": resultados
    }


def obtener_citas_mascota(mascota_id: int):

    response = requests.get(
        f"{CITAS_URL}/mascota/{mascota_id}"
    )

    response.raise_for_status()

    return {
        "mascota_id": mascota_id,
        "citas": response.json()
    }   
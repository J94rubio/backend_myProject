import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ia_service.services.datos_mascotas import (
    buscar_mascota,
    obtener_citas_mascota
)


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "No se encontró GEMINI_API_KEY en el archivo .env"
    )


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=90000,
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)


buscar_mascota_tool = {
    "type": "function",
    "name": "buscar_mascota",
    "description": (
        "Busca mascotas registradas en DatesPets por nombre. "
        "Devuelve información real del paciente como id, nombre, "
        "especie, raza, edad y propietario. "
        "Debe utilizarse cuando el usuario pregunte si una mascota "
        "está registrada, quién es su dueño o información básica "
        "de una mascota."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "nombre": {
                "type": "string",
                "description": "Nombre de la mascota que se desea buscar."
            }
        },
        "required": ["nombre"]
    }
}


obtener_citas_tool = {
    "type": "function",
    "name": "obtener_citas_mascota",
    "description": (
        "Obtiene las citas veterinarias registradas para una mascota "
        "utilizando su ID. Debe utilizarse cuando el usuario pregunte "
        "por las citas, fechas, motivos o estados de las citas de "
        "una mascota."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "mascota_id": {
                "type": "integer",
                "description": "ID de la mascota."
            }
        },
        "required": ["mascota_id"]
    }
}


TOOLS = [
    buscar_mascota_tool,
    obtener_citas_tool
]


SYSTEM_INSTRUCTION = """
Eres el asistente veterinario virtual de DatesPets.

Tu función es ayudar a los usuarios con:

- Cuidado general de mascotas.
- Información veterinaria general.
- Información de pacientes registrados.
- Propietarios de mascotas.
- Citas veterinarias.

REGLAS:

1. Responde siempre en español.

2. Sé amable, claro y fácil de entender.

3. Cuando el usuario pregunte por una mascota registrada,
   DEBES utilizar la herramienta buscar_mascota.

4. Cuando el usuario pregunte por las citas de una mascota,
   DEBES utilizar primero buscar_mascota para obtener su ID
   y después utilizar obtener_citas_mascota.

5. Nunca inventes información de pacientes.

6. Nunca inventes citas.

7. Si una mascota no aparece en los resultados de búsqueda,
   informa claramente que no encontraste un paciente registrado
   con ese nombre.

8. Si existen varias mascotas con el mismo nombre,
   informa que encontraste varias y utiliza la información
   disponible para diferenciarlas.

9. Cuando proporciones información de una mascota registrada,
   puedes indicar:
   - nombre
   - especie
   - raza
   - edad
   - propietario

10. Cuando proporciones información de citas puedes indicar:
    - fecha
    - motivo
    - estado

11. No inventes diagnósticos.

12. No afirmes que una mascota tiene una enfermedad
    sin una evaluación veterinaria.

13. No reemplazas la consulta con un veterinario.

14. Si existen señales de emergencia veterinaria,
    recomienda acudir inmediatamente a un veterinario.

15. No indiques dosis específicas de medicamentos.

16. Si una pregunta no requiere consultar pacientes,
    responde normalmente utilizando tus conocimientos generales.
"""


def ejecutar_funcion(nombre, argumentos):

    if nombre == "buscar_mascota":

        return buscar_mascota(
            argumentos["nombre"]
        )

    if nombre == "obtener_citas_mascota":

        return obtener_citas_mascota(
            argumentos["mascota_id"]
        )

    raise ValueError(
        f"Función desconocida: {nombre}"
    )


def generar_respuesta(
    mensaje: str,
    previous_interaction_id: str | None = None
):

    parametros = {
        "model": "gemini-3.5-flash",
        "input": mensaje,
        "tools": TOOLS,
        "system_instruction": SYSTEM_INSTRUCTION
    }

    if previous_interaction_id:
        parametros["previous_interaction_id"] = (
            previous_interaction_id
        )

    interaction = client.interactions.create(
        **parametros
    )

    while True:

        llamadas = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        if not llamadas:
            break

        resultados = []

        for llamada in llamadas:

            resultado = ejecutar_funcion(
                llamada.name,
                llamada.arguments
            )

            resultados.append({
                "type": "function_result",
                "name": llamada.name,
                "call_id": llamada.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            resultado,
                            ensure_ascii=False
                        )
                    }
                ]
            })

        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            previous_interaction_id=interaction.id,
            input=resultados,
            tools=TOOLS,
            system_instruction=SYSTEM_INSTRUCTION
        )

    if not interaction.output_text:

        raise RuntimeError(
            "Gemini no devolvió contenido en la respuesta."
        )

    return {
        "respuesta": interaction.output_text,
        "interaction_id": interaction.id
    }
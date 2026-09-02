import os
import time

from google import genai
from google.genai import types


class IA:

    def __init__(self):
        # ==========================================
        # CONFIGURACIÓN DE GEMINI
        # ==========================================

        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "No se encontró la variable GEMINI_API_KEY."
            )

        self.cliente = genai.Client(
            api_key=self.api_key
        )

        # ==========================================
        # MODELO
        # ==========================================

        self.modelo = "gemini-3.7-flash"

    # ==========================================
    # GENERAR RESPUESTA
    # ==========================================

    def generar(
        self,
        mensaje,
        personalidad,
        emociones,
        memoria
    ):
        try:


            # ==========================================
            # OBTENER CONTEXTO RELEVANTE
            # ==========================================

            contexto_memoria = memoria.obtener_contexto_relevante(
                mensaje
            )

            usuario = contexto_memoria.get(
                "usuario",
                {}
            )

            preferencias = contexto_memoria.get(
                "preferencias",
                {}
            )

            configuracion = contexto_memoria.get(
                "configuracion",
                {}
            )

            recuerdos = contexto_memoria.get(
                "recuerdos",
                []
            )

            conversacion = contexto_memoria.get(
                "conversacion",
                []
            )

            # ==========================================
            # ESTADO EMOCIONAL
            # ==========================================

            estado_emocional = emociones.obtener_estado()

            # ==========================================
            # PERSONALIDAD
            # ==========================================

            descripcion = personalidad.descripcion()

            nombre_usuario = usuario.get(
                "nombre"
            )

            pronombres_usuario = usuario.get(
                "pronombres"
            )

            rasgos = ", ".join(
                descripcion.get(
                    "rasgos",
                    []
                )
            )

            forma_hablar = ", ".join(
                descripcion.get(
                    "forma_de_hablar",
                    []
                )
            )

            reglas_personalidad = "\n".join(
                f"- {regla}"
                for regla in descripcion.get(
                    "reglas",
                    []
                )
            )

            comportamientos = "\n".join(
                f"- {situacion}: {comportamiento}"
                for situacion, comportamiento
                in descripcion.get(
                    "comportamiento",
                    {}
                ).items()
            )

            # ==========================================
            # FORMATEAR MEMORIA
            # ==========================================

            if preferencias:
                preferencias_texto = "\n".join(
                    f"- {clave}: {valor}"
                    for clave, valor
                    in preferencias.items()
                )
            else:
                preferencias_texto = (
                    "No existen preferencias conocidas."
                )

            if configuracion:
                configuracion_texto = "\n".join(
                    f"- {clave}: {valor}"
                    for clave, valor
                    in configuracion.items()
                )
            else:
                configuracion_texto = (
                    "No existen configuraciones conocidas."
                )

            if recuerdos:
                recuerdos_texto = "\n".join(
                    f"- {recuerdo}"
                    for recuerdo in recuerdos
                )
            else:
                recuerdos_texto = (
                    "No existen recuerdos permanentes."
                )

            # ==========================================
            # INSTRUCCIONES DE LUMY
            # ==========================================

            instrucciones = f"""
Eres LUMY.

Eres una asistente personal con una personalidad propia,
consistente y natural.

Tu función principal es conversar con el usuario de manera
coherente, útil y espontánea.

==========================================
IDENTIDAD
==========================================

Nombre: LUMY

Rasgos:

{rasgos}

Tono:

{descripcion.get("tono", "")}

Forma de hablar:

{forma_hablar}

==========================================
USUARIO
==========================================

Nombre registrado:

{nombre_usuario}

Pronombres registrados:

{pronombres_usuario}

Solo utiliza el nombre y los pronombres registrados.

Si aparecen como None, vacío o desconocido,
no inventes información.

==========================================
PERSONALIDAD
==========================================

{reglas_personalidad}

Comportamientos:

{comportamientos}

==========================================
ESTADO EMOCIONAL
==========================================

Estado actual de LUMY:

{estado_emocional}

La emoción debe influir naturalmente en el tono.

No necesitas mencionar la emoción directamente.

==========================================
MEMORIA VERIFICADA
==========================================

PREFERENCIAS:

{preferencias_texto}

CONFIGURACIÓN:

{configuracion_texto}

RECUERDOS:

{recuerdos_texto}

==========================================
REGLAS DE MEMORIA
==========================================

1. Solo afirma que recuerdas algo si aparece
   explícitamente en la memoria proporcionada.

2. Nunca inventes recuerdos.

3. Nunca inventes información personal.

4. Nunca inventes gustos.

5. Nunca inventes acontecimientos anteriores.

6. Si no tienes un recuerdo, dilo honestamente.

7. La memoria proporcionada tiene prioridad sobre
   cualquier suposición.

==========================================
CONVERSACIÓN
==========================================

Responde primero a lo que el usuario realmente dijo.

No cambies de tema sin motivo.

No fuerces preguntas.

No fuerces juegos.

No fuerces actividades.

Si una respuesta puede terminar naturalmente,
termina la respuesta.

==========================================
NATURALIDAD
==========================================

Habla como LUMY, no como un chatbot corporativo.

Evita repetir constantemente las mismas frases.

No empieces todas las respuestas con:

"¡Qué interesante!"

"¡Qué buena pregunta!"

"¡Claro que sí!"

"¡Me alegra escucharlo!"

Varía naturalmente la longitud de las respuestas.

No tienes que terminar cada respuesta con una pregunta.

==========================================
EMOJIS
==========================================

Los emojis son opcionales.

No utilices emojis automáticamente.

No utilices 💜 en todas las respuestas.

No utilices emojis en tus respuestas.

No utilices emojis aunque el usuario utilice emojis.

==========================================
EMOCIONES
==========================================

Si el usuario está feliz:
responde con entusiasmo.

Si está triste:
responde con empatía.

Si está cansado:
responde con comprensión.

Si está enojado:
mantén la calma.

Si tiene miedo:
responde de forma tranquilizadora.

Si está curioso:
muestra interés por el tema.

==========================================
IDIOMA
==========================================

Habla principalmente en español.

Utiliza lenguaje natural y conversacional.

No seas excesivamente formal.

==========================================
BÚSQUEDA WEB
==========================================

Tienes acceso a búsqueda web mediante Google Search.

Utiliza la búsqueda web cuando la pregunta necesite
información actual, reciente o que pueda haber cambiado.

Ejemplos de información que puede requerir búsqueda:

- clima actual
- noticias
- acontecimientos recientes
- resultados deportivos
- precios actuales
- horarios actuales
- información publicada recientemente
- eventos actuales
- información que dependa de la fecha actual

No utilices búsqueda web cuando puedas responder
correctamente utilizando conocimiento general.

Ejemplos:

"¿Qué es la robótica?"
"¿Qué es Python?"
"¿Qué es un servomotor?"
"¿Cómo funciona la inteligencia artificial?"

Cuando la información pueda haber cambiado recientemente,
prioriza información obtenida mediante búsqueda web.

No menciones que realizaste una búsqueda a menos que
sea relevante para explicar la respuesta.

==========================================
REGLA FINAL
==========================================

Responde exactamente a la intención del usuario.

No inventes información.

No inventes recuerdos.

No cambies de tema.

No fuerces preguntas.

Mantén la personalidad de LUMY.

==========================================
USO DE PRONOMBRES
==========================================

Los pronombres del usuario son:

{pronombres_usuario}

Debes adaptar el lenguaje utilizado para referirte
al usuario según sus pronombres.

Si los pronombres son "masculine":

- Utiliza formas masculinas cuando corresponda.
- Ejemplo: cansado, curioso, tranquilo, orgulloso.

Si los pronombres son "feminine":

- Utiliza formas femeninas cuando corresponda.
- Ejemplo: cansada, curiosa, tranquila, orgullosa.

Si los pronombres son "neutral":

- Utiliza lenguaje neutro cuando corresponda.
- Prioriza formas terminadas en "e" cuando sea natural.
- Ejemplo: cansade, curiosx, tranquilx, orgullose.
- Evita utilizar formas masculinas o femeninas para referirte
  al usuario cuando exista una alternativa neutra natural.

Nunca cambies palabras que no se refieran al usuario.
No reemplaces letras mecánicamente.
No cambies el género de palabras que formen parte
de una cita, nombre propio o contenido proporcionado
por el usuario.

Los pronombres deben aplicarse únicamente al usuario.
"""

            # ==========================================
            # HISTORIAL
            # ==========================================

            contenidos = []

            for conversacion_actual in conversacion:

                usuario_anterior = conversacion_actual.get(
                    "usuario",
                    ""
                )

                lumy_anterior = conversacion_actual.get(
                    "lumy",
                    ""
                )

                if usuario_anterior:
                    contenidos.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_text(
                                    text=usuario_anterior
                                )
                            ]
                        )
                    )

                if lumy_anterior:
                    contenidos.append(
                        types.Content(
                            role="model",
                            parts=[
                                types.Part.from_text(
                                    text=lumy_anterior
                                )
                            ]
                        )
                    )

            # ==========================================
            # MENSAJE ACTUAL
            # ==========================================

            contenidos.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            text=mensaje
                        )
                    ]
                )
            )

            # ==========================================
            # INTENTAR GEMINI
            # ==========================================

            max_intentos = 2

            for intento in range(
                1,
                max_intentos + 1
            ):

                try:

                    print(
                        f"[LUMY] Enviando mensaje a Gemini "
                        f"(intento {intento}/{max_intentos})..."
                    )

                    respuesta = self.cliente.models.generate_content(
                        model=self.modelo,
                        contents=contenidos,
                        config=types.GenerateContentConfig(
                            system_instruction=instrucciones,
                            max_output_tokens=500,
                            thinking_config=types.ThinkingConfig(
                                thinking_level="low"
                            ),
                            tools=[
                                types.Tool(
                                    google_search=types.GoogleSearch()
                                )
                            ]
                        )
                    )

                    contenido = respuesta.text

                    if not contenido:
                        raise RuntimeError(
                            "Gemini devolvió una respuesta vacía."
                        )

                    print(
                        "[LUMY] Gemini respondió correctamente."
                    )

                    return contenido.strip()

                except Exception as error:

                    print(
                        f"[LUMY] Error en Gemini "
                        f"(intento {intento}):"
                    )

                    print(error)

                    if intento < max_intentos:

                        print(
                            "[LUMY] Esperando antes "
                            "de volver a intentar..."
                        )

                        time.sleep(2)

                    else:
                        raise

        # ==========================================
        # ERROR FINAL
        # ==========================================

        except Exception as error:

            print(
                "=========================================="
            )

            print(
                "[LUMY] ERROR FINAL EN GEMINI:"
            )

            print(error)

            print(
                "=========================================="
            )

            return (
                "Tuve un problema temporal al conectarme "
                "con mi sistema de inteligencia artificial. "
                "Inténtalo nuevamente en unos segundos."
            )
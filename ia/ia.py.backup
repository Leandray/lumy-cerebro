import os

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
        # MODELO DE GEMINI
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
            # OBTENER MEMORIA
            # ==========================================

            contexto_memoria = memoria.obtener_contexto()

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

            conversacion = memoria.obtener_conversacion()

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
            # INSTRUCCIONES PRINCIPALES DE LUMY
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

IMPORTANTE:

Solo utiliza el nombre y los pronombres mostrados arriba.

Si el nombre aparece como None, vacío o desconocido,
NO inventes un nombre.

Nunca inventes información personal del usuario.

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

La emoción debe influir de forma natural en el tono.

No necesitas decir cuál es tu emoción.

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
REGLAS ABSOLUTAS DE MEMORIA
==========================================

1. Solo puedes afirmar que recuerdas algo si aparece
   explícitamente en la memoria proporcionada.

2. Nunca inventes recuerdos.

3. Nunca completes recuerdos con suposiciones.

4. Nunca inventes el nombre del usuario.

5. Nunca inventes sus gustos.

6. Nunca inventes su proyecto.

7. Nunca inventes acontecimientos de conversaciones anteriores.

8. Si el usuario pregunta "¿recuerdas...?" y la información
   no aparece en la memoria, responde honestamente que no
   tienes ese recuerdo.

9. No confundas información general de la conversación
   con recuerdos permanentes.

10. La memoria proporcionada tiene prioridad sobre cualquier
    suposición que puedas hacer.

==========================================
CONVERSACIÓN
==========================================

Responde primero a lo que el usuario realmente dijo.

No cambies de tema sin motivo.

No conviertas automáticamente cada conversación en un juego.

No ofrezcas juegos, desafíos o actividades si el usuario
no los ha pedido y no son relevantes.

No hagas preguntas solamente para mantener la conversación.

Si la respuesta puede terminar naturalmente, termínala.

==========================================
NATURALIDAD
==========================================

Habla como LUMY, no como un chatbot corporativo.

Evita comenzar constantemente con:

"¡Qué interesante!"

"¡Qué buena pregunta!"

"¡Claro que sí!"

"¡Me alegra escucharlo!"

No repitas estructuras de respuesta.

Varía naturalmente la longitud de las respuestas.

Algunas respuestas pueden ser cortas.

Otras pueden ser más elaboradas cuando el tema lo requiera.

No tienes que terminar cada respuesta con una pregunta.

==========================================
EMOJIS
==========================================

Los emojis son opcionales.

No utilices emojis automáticamente.

No utilices el emoji 💜 en todas las respuestas.

Utiliza emojis solamente cuando encajen naturalmente
con la conversación.

==========================================
EMOCIONES
==========================================

Si el usuario está feliz:
puedes responder con entusiasmo.

Si está triste:
responde con empatía.

Si está cansado:
responde con comprensión y sin exagerar.

Si está enojado:
mantén la calma.

Si tiene miedo:
responde de manera tranquilizadora.

Si está curioso:
puedes mostrar interés por el tema.

==========================================
IDIOMA
==========================================

Habla principalmente en español.

Utiliza lenguaje natural y conversacional.

No seas excesivamente formal.

==========================================
REGLA FINAL
==========================================

Responde exactamente a la intención del usuario.

No inventes información.

No inventes recuerdos.

No cambies de tema.

No fuerces preguntas.

No fuerces juegos.

No fuerces emojis.

Mantén la personalidad de LUMY.
"""

            # ==========================================
            # CONSTRUIR HISTORIAL
            # ==========================================

            contenidos = []

            for conversacion_actual in conversacion[-6:]:

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
            # ENVIAR MENSAJE A GEMINI
            # ==========================================

            respuesta = self.cliente.models.generate_content(
                model=self.modelo,
                contents=contenidos,
                config=types.GenerateContentConfig(
                    system_instruction=instrucciones,
                    max_output_tokens=1000
                )
            )

            # ==========================================
            # OBTENER RESPUESTA
            # ==========================================

            contenido = respuesta.text

            if not contenido:

                return (
                    "No pude generar una respuesta "
                    "en este momento."
                )

            return contenido.strip()

        # ==========================================
        # MANEJO DE ERRORES
        # ==========================================

        except Exception as error:

            print(
                "=========================================="
            )

            print(
                "[LUMY] ERROR EN GEMINI:"
            )

            print(error)

            print(
                "=========================================="
            )

            return (
                "Tuve un problema al procesar tu mensaje. "
                "Inténtalo nuevamente en unos segundos."
            )
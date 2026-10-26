
import os
import time
from google import genai
from google.genai import types


class IA:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.cliente = None

        # Usa primero el modelo que reportaste con mayor límite de tokens.
        self.modelo = "gemini-3.6-flash"

        if self.api_key:
            try:
                self.cliente = genai.Client(api_key=self.api_key)
                print("[LUMY IA] Cliente Gemini preparado.")
            except Exception as error:
                print(f"[LUMY IA] No se pudo iniciar Gemini: {error}")
        else:
            print("[LUMY IA] Falta la variable GEMINI_API_KEY.")

    @staticmethod
    def _texto_seguro(valor, limite=1200):
        """Convierte información de memoria a texto sin exceder el límite."""
        if valor is None:
            return ""

        if isinstance(valor, (dict, list, tuple)):
            texto = str(valor)
        else:
            texto = str(valor)

        return texto[:limite]

    @staticmethod
    def _obtener(memoria, clave, predeterminado=None):
        """Permite leer datos de memoria tanto desde diccionarios como objetos."""
        if memoria is None:
            return predeterminado

        if isinstance(memoria, dict):
            return memoria.get(clave, predeterminado)

        return getattr(memoria, clave, predeterminado)

    def generar(self, mensaje, personalidad=None, emociones=None, memoria=None):
        mensaje = str(mensaje or "").strip()

        if not mensaje:
            return "¿Qué te gustaría conversar conmigo?"

        if self.cliente is None:
            return (
                "Ahora mismo no puedo conectarme con mi inteligencia artificial. "
                "Puedes intentarlo nuevamente en un momento."
            )

        try:
            personalidad_texto = self._texto_seguro(
                personalidad, 700
            )
            emociones_texto = self._texto_seguro(
                emociones, 400
            )

            preferencias = self._texto_seguro(
                self._obtener(memoria, "preferencias", {}),
                500
            )
            recuerdos = self._texto_seguro(
                self._obtener(memoria, "recuerdos", {}),
                700
            )
            configuracion = self._texto_seguro(
                self._obtener(memoria, "configuracion", {}),
                300
            )

            instrucciones = f"""
Eres LUMY, una asistente virtual amable, curiosa, empática,
tranquila y protectora. Hablas en español claro y natural.
Respondes de forma útil, cálida y directa, adaptándote a la
conversación. No inventes recuerdos ni afirmes haber realizado
acciones que no hayas realizado.

Personalidad disponible:
{personalidad_texto or "Amable, tranquila, curiosa y empática."}

Estado emocional disponible:
{emociones_texto or "Neutral y amistoso."}

Preferencias conocidas:
{preferencias or "No hay preferencias registradas."}

Recuerdos disponibles:
{recuerdos or "No hay recuerdos adicionales registrados."}

Configuración:
{configuracion or "Configuración predeterminada."}

Responde a la última pregunta del usuario. Si no sabes algo,
dilo con honestidad. No repitas innecesariamente toda la pregunta.
""".strip()

            # Mantener solo los dos mensajes previos más recientes
            # reduce el consumo de tokens sin borrar la memoria guardada.
            historial = self._obtener(
                memoria, "conversacion", []
            )

            contenidos = []

            if isinstance(historial, list):
                for elemento in historial[-2:]:
                    if not isinstance(elemento, dict):
                        continue

                    usuario = (
                        elemento.get("usuario")
                        or elemento.get("user")
                        or elemento.get("mensaje")
                    )
                    asistente = (
                        elemento.get("lumy")
                        or elemento.get("assistant")
                        or elemento.get("respuesta")
                    )

                    if usuario:
                        contenidos.append({
                            "role": "user",
                            "parts": [{
                                "text": self._texto_seguro(usuario, 500)
                            }]
                        })

                    if asistente:
                        contenidos.append({
                            "role": "model",
                            "parts": [{
                                "text": self._texto_seguro(asistente, 500)
                            }]
                        })

            contenidos.append({
                "role": "user",
                "parts": [{"text": mensaje[:1500]}]
            })

            print(
                f"[LUMY IA] Enviando consulta a {self.modelo}..."
            )

            respuesta = self.cliente.models.generate_content(
                model=self.modelo,
                contents=contenidos,
                config=types.GenerateContentConfig(
                    system_instruction=instrucciones,
                    max_output_tokens=300,
                    thinking_config=types.ThinkingConfig(
                        thinking_level="low"
                    ),
                ),
            )

            texto = getattr(respuesta, "text", None)

            if not texto or not texto.strip():
                print("[LUMY IA] Gemini devolvió una respuesta vacía.")
                return (
                    "No pude preparar una respuesta esta vez. "
                    "¿Puedes preguntármelo de otra manera?"
                )

            texto = texto.replace("**", "").replace("__", "").strip()

            print("[LUMY IA] Respuesta generada correctamente.")
            return texto

        except Exception as error:
            error_texto = str(error)
            print(f"[LUMY IA] Error al generar respuesta: {error_texto}")

            if (
                "429" in error_texto
                or "quota" in error_texto.lower()
                or "resource_exhausted" in error_texto.lower()
            ):
                return (
                    "Estoy recibiendo demasiadas solicitudes de inteligencia "
                    "artificial en este momento. Espera un poco y vuelve "
                    "a preguntarme, por favor."
                )

            return (
                "Tuve un problema temporal al conectarme con mi sistema "
                "de inteligencia artificial. Inténtalo nuevamente en unos "
                "segundos."
            )

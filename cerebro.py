from entrada import Entrada
from respuesta import Respuesta
from memoria.memoria import Memoria
from emociones.emociones import Emociones
from personalidad.personalidad import Personalidad


class Cerebro:

    def __init__(self, uid):
        self.uid = uid
        self.entrada = Entrada()
        self.memoria = Memoria(uid)
        self.emociones = Emociones()
        self.personalidad = Personalidad()
        self.respuesta = Respuesta()

    # ==================================================
    # PROCESAR MENSAJE
    # ==================================================

    def procesar(self, mensaje):

        mensaje = self.entrada.recibir(mensaje)

        if not mensaje:
            return {
                "respuesta": "No recibí ningún mensaje.",
                "accion": None,
                "requiere_confirmacion": False
            }

        # ==================================================
        # GENERAR RESPUESTA
        # ==================================================

        resultado = self.respuesta.generar(
            mensaje,
            self.personalidad,
            self.emociones,
            self.memoria
        )

        # ==================================================
        # COMPROBAR SI ES UNA ACCIÓN
        # ==================================================

        if isinstance(resultado, dict):

            texto_respuesta = resultado.get(
                "respuesta",
                ""
            )

            # ==================================================
            # GUARDAR CONVERSACIÓN
            # ==================================================

            self.memoria.guardar_mensaje(
                mensaje,
                texto_respuesta
            )

            return resultado

        # ==================================================
        # RESPUESTA NORMAL
        # ==================================================

        self.memoria.guardar_mensaje(
            mensaje,
            resultado
        )

        return {
            "respuesta": resultado,
            "accion": None,
            "requiere_confirmacion": False
        }
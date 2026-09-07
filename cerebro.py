from entrada import Entrada
from respuesta import Respuesta
from memoria.memoria import Memoria
from emociones.emociones import Emociones
from personalidad.personalidad import Personalidad


class Cerebro:

    def __init__(self, uid, notificar=None):

        self.uid = uid
        self.notificar = notificar

        self.entrada = Entrada()
        self.memoria = Memoria(uid)
        self.emociones = Emociones()
        self.personalidad = Personalidad()

        self.respuesta = Respuesta(
            notificar=self.enviar_notificacion
        )

    # ==================================================
    # ENVIAR NOTIFICACIÓN
    # ==================================================

    def enviar_notificacion(self, notificacion):

        if self.notificar:

            self.notificar(
                self.uid,
                notificacion
            )

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

        resultado = self.respuesta.generar(
            mensaje,
            self.personalidad,
            self.emociones,
            self.memoria
        )

        # ----------------------------------------------
        # RESPUESTA CON ACCIÓN
        # ----------------------------------------------

        if isinstance(resultado, dict):

            texto_respuesta = resultado.get(
                "respuesta",
                ""
            )

            self.memoria.guardar_mensaje(
                mensaje,
                texto_respuesta
            )

            return resultado

        # ----------------------------------------------
        # RESPUESTA NORMAL
        # ----------------------------------------------

        self.memoria.guardar_mensaje(
            mensaje,
            resultado
        )

        return {
            "respuesta": resultado,
            "accion": None,
            "requiere_confirmacion": False
        }
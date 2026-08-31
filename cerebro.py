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

            return "No recibí ningún mensaje."

        # ==================================================
        # GENERAR RESPUESTA
        # ==================================================

        respuesta = self.respuesta.generar(
            mensaje,
            self.personalidad,
            self.emociones,
            self.memoria
        )

        # ==================================================
        # GUARDAR CONVERSACIÓN
        # ==================================================

        self.memoria.guardar_mensaje(
            mensaje,
            respuesta
        )

        return respuesta
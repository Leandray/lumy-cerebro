import threading
import time


class Temporizador:

    def __init__(self, al_terminar=None):

        self.activo = False
        self.duracion = 0
        self.inicio = None
        self.finalizacion = None
        self.hilo = None

        self.al_terminar = al_terminar

    # ==================================================
    # CREAR TEMPORIZADOR
    # ==================================================

    def crear(self, segundos):

        if segundos <= 0:

            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        # Cancelar temporizador anterior
        self.activo = False

        self.duracion = segundos

        self.inicio = time.time()

        self.finalizacion = (
            self.inicio + segundos
        )

        self.activo = True

        self.hilo = threading.Thread(
            target=self._esperar,
            daemon=True
        )

        self.hilo.start()

    # ==================================================
    # ESPERAR
    # ==================================================

    def _esperar(self):

        while self.activo:

            restante = (
                self.finalizacion - time.time()
            )

            if restante <= 0:

                self.activo = False

                print(
                    "[LUMY] 🔔 El temporizador ha terminado."
                )

                # --------------------------------------
                # NOTIFICAR A LUMY
                # --------------------------------------

                if self.al_terminar:

                    try:

                        self.al_terminar()

                    except Exception as error:

                        print(
                            "[LUMY] Error al enviar "
                            "notificación:",
                            error
                        )

                break

            time.sleep(0.5)

    # ==================================================
    # CONSULTAR
    # ==================================================

    def consultar(self):

        if not self.activo:

            return None

        restante = (
            self.finalizacion - time.time()
        )

        if restante <= 0:

            self.activo = False

            return None

        return int(restante)

    # ==================================================
    # CANCELAR
    # ==================================================

    def cancelar(self):

        if not self.activo:

            return False

        self.activo = False

        return True

    # ==================================================
    # ESTADO
    # ==================================================

    def esta_activo(self):

        return self.activo
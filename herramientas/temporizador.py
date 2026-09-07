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

    def crear(self, segundos):

        if segundos <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        # Si ya había uno activo, lo cancelamos
        self.activo = False

        self.duracion = segundos
        self.inicio = time.time()
        self.finalizacion = self.inicio + segundos
        self.activo = True

        self.hilo = threading.Thread(
            target=self._esperar,
            daemon=True
        )

        self.hilo.start()

    def _esperar(self):

        while self.activo:

            restante = self.finalizacion - time.time()

            if restante <= 0:

                self.activo = False

                print(
                    "[LUMY] 🔔 El temporizador ha terminado."
                )

                # Avisar a la API
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

    def consultar(self):

        if not self.activo:
            return None

        restante = self.finalizacion - time.time()

        if restante <= 0:

            self.activo = False

            return None

        return int(restante)

    def cancelar(self):

        if not self.activo:
            return False

        self.activo = False

        return True

    def esta_activo(self):

        return self.activo
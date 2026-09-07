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

        print(
            f"[LUMY] ⏱️ Creando temporizador de {segundos} segundos."
        )

        # Cancelar temporizador anterior
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

        print(
            "[LUMY] ⏱️ Hilo del temporizador iniciado."
        )

    # ==================================================
    # ESPERAR
    # ==================================================

    def _esperar(self):

        print(
            "[LUMY] ⏳ Temporizador esperando..."
        )

        while self.activo:

            restante = (
                self.finalizacion - time.time()
            )

            if restante <= 0:

                self.activo = False

                print(
                    "[LUMY] 🔔 EL TEMPORIZADOR HA TERMINADO."
                )

                # --------------------------------------
                # NOTIFICAR
                # --------------------------------------

                if self.al_terminar:

                    print(
                        "[LUMY] 📢 Ejecutando callback de notificación..."
                    )

                    try:

                        self.al_terminar()

                        print(
                            "[LUMY] ✅ Callback ejecutado correctamente."
                        )

                    except Exception as error:

                        print(
                            "[LUMY] ❌ Error al enviar notificación:"
                        )

                        print(error)

                else:

                    print(
                        "[LUMY] ⚠️ No existe callback de notificación."
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

        print(
            "[LUMY] ⏹️ Temporizador cancelado."
        )

        return True

    # ==================================================
    # ESTADO
    # ==================================================

    def esta_activo(self):

        return self.activo
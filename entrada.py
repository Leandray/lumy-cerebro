class Entrada:
    def recibir(self, mensaje):
        if not mensaje:
            return None

        mensaje = mensaje.strip()

        if not mensaje:
            return None

        return mensaje
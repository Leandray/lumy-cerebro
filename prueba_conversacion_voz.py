from voz import Voz
from cerebro import Cerebro


# ==========================================
# CONFIGURACIÓN
# ==========================================

# Pon aquí temporalmente el UID de un usuario
# que exista en Firebase.
UID = "0AYfiNFl6sW2nVouAL7qXFG3xJx2"


# ==========================================
# CREAR COMPONENTES
# ==========================================

voz = Voz()
cerebro = Cerebro(UID)


print("================================")
print("    LUMY - CONVERSACIÓN POR VOZ")
print("================================")
print("Habla con LUMY.")
print("Di 'salir' para terminar.")
print("================================")


# ==========================================
# BUCLE DE CONVERSACIÓN
# ==========================================

while True:

    # --------------------------------------
    # ESCUCHAR
    # --------------------------------------

    mensaje = voz.escuchar()

    if not mensaje:
        continue

    # --------------------------------------
    # COMPROBAR SALIDA
    # --------------------------------------

    if mensaje.lower().strip() in [
        "salir",
        "adiós",
        "adios"
    ]:

        voz.hablar("Hasta luego.")
        break

    # --------------------------------------
    # PROCESAR CON EL CEREBRO
    # --------------------------------------

    print("\n🧠 Procesando con el cerebro de LUMY...")

    respuesta = cerebro.procesar(mensaje)

    # --------------------------------------
    # HABLAR
    # --------------------------------------

    voz.hablar(respuesta)
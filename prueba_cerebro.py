from cerebro import Cerebro


# ==========================================
# UID DEL USUARIO
# ==========================================

UID = "TU_UID_REAL"


# ==========================================
# CREAR CEREBRO
# ==========================================

print("================================")
print("       INICIANDO LUMY")
print("================================")

cerebro = Cerebro(UID)

print("Cerebro cargado correctamente.")
print()


# ==========================================
# CONVERSACIÓN
# ==========================================

mensaje = input("Tú: ")

print()
print("LUMY está pensando...")
print()

respuesta = cerebro.procesar(mensaje)

print("LUMY:", respuesta)
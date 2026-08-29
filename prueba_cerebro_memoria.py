from cerebro import Cerebro


# ==========================================
# CONFIGURACIÓN
# ==========================================

UID = "prueba_Lumi"


# ==========================================
# CREAR CEREBRO
# ==========================================

cerebro = Cerebro(UID)


print("\n==========================================")
print("PRUEBA CEREBRO + MEMORIA")
print("==========================================\n")


# ==========================================
# MOSTRAR MEMORIA
# ==========================================

print("USUARIO:")
print(cerebro.memoria.obtener_usuario())

print("\nPREFERENCIAS:")
print(cerebro.memoria.preferencias)

print("\nCONFIGURACIÓN:")
print(cerebro.memoria.configuracion)

print("\nRECUERDOS:")
print(cerebro.memoria.obtener_recuerdos())

print("\nCONVERSACIÓN:")
print(cerebro.memoria.obtener_conversacion())


# ==========================================
# PROCESAR MENSAJE
# ==========================================

print("\n==========================================")
print("MENSAJE")
print("==========================================")

respuesta = cerebro.procesar(
    "¿Cuál es mi color favorito?"
)

print("\nLUMY:")
print(respuesta)


print("\n==========================================")
print("PRUEBA TERMINADA")
print("==========================================")
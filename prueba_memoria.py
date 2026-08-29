from memoria.memoria import Memoria


# ==========================================
# CONFIGURACIÓN
# ==========================================

UID = "prueba_Lumi"


# ==========================================
# CREAR MEMORIA
# ==========================================

memoria = Memoria(UID)


print("\n==========================================")
print("PRUEBA DE RECUPERACIÓN DE MEMORIA")
print("==========================================\n")


# ==========================================
# MOSTRAR USUARIO
# ==========================================

print("Usuario:")
print(memoria.obtener_usuario())


# ==========================================
# RECUPERAR PREFERENCIA
# ==========================================

print("\nColor favorito recuperado:")

print(
    memoria.obtener_preferencia("color_favorito")
)


# ==========================================
# RECUPERAR RECUERDOS
# ==========================================

print("\nRecuerdos recuperados:")

print(
    memoria.obtener_recuerdos()
)


# ==========================================
# MOSTRAR CONVERSACIÓN
# ==========================================

print("\nConversación recuperada:")

print(
    memoria.obtener_conversacion()
)


print("\n==========================================")
print("RECUPERACIÓN TERMINADA")
print("==========================================")
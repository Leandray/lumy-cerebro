from emociones.emociones import Emociones


emociones = Emociones()


print("==========================================")
print("       PRUEBA DEL DETECTOR EMOCIONAL")
print("==========================================")


mensajes = [
    "Hola LUMY",
    "Jajaja eres muy divertida",
    "Estoy muy triste hoy",
    "Esto es injusto, estoy enojado",
    "Tengo mucho miedo",
    "WOW no puedo creerlo",
    "¿Cómo funciona un agujero negro?"
]


for mensaje in mensajes:

    print("\n------------------------------------------")
    print("Mensaje:", mensaje)

    detectada = emociones.detectar(mensaje)

    print("Emoción detectada:", detectada)
    print("Estado actual:", emociones.obtener_estado())


print("\n==========================================")
print("          PRUEBA FINALIZADA")
print("==========================================")

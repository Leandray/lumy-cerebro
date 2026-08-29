from voz import Voz


voz = Voz()


print("================================")
print("       PRUEBA DE VOZ LUMY")
print("================================")


texto = voz.escuchar()


if texto:

    respuesta = f"Escuché que dijiste: {texto}"

    voz.hablar(respuesta)

else:

    print("No se pudo reconocer la voz.")
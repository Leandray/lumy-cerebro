from emociones.emociones import Emociones


emociones = Emociones()


print("==========================================")
print("      PRUEBA DEL SISTEMA EMOCIONAL")
print("==========================================")


print("\nESTADO INICIAL")
print(emociones.obtener_estado())


print("\n--- LUMY SE PONE FELIZ ---")

emociones.modificar("felicidad", 30)

print(emociones.obtener_estado())


print("\n--- LUMY SE PONE TRISTE ---")

emociones.modificar("tristeza", 60)

print(emociones.obtener_estado())


print("\n--- LUMY SE PONE CURIOSA ---")

emociones.modificar("curiosidad", 50)

print(emociones.obtener_estado())


print("\n--- LUMY SE CALMA ---")

emociones.calmar(20)

print(emociones.obtener_estado())


print("\n==========================================")
print("        PRUEBA FINALIZADA")
print("==========================================")
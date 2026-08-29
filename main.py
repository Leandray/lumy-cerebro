from cerebro import Cerebro


def main():

    lumy = Cerebro()

    print("================================")
    print("        LUMY - CEREBRO")
    print("================================")
    print("Escribe 'salir' para terminar.")
    print()

    while True:

        mensaje = input("Tú: ")

        if mensaje.lower() == "salir":
            print("LUMY: Hasta luego. 💜")
            break

        respuesta = lumy.procesar(mensaje)

        print("LUMY:", respuesta)


if __name__ == "__main__":
    main()
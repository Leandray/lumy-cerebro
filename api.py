from flask import Flask, request, jsonify
from flask_cors import CORS
from cerebro import Cerebro


app = Flask(__name__)
CORS(app)


# ==================================================
# CEREBROS ACTIVOS
# ==================================================

# Guarda un Cerebro por cada usuario.
# Esto permite conservar el estado de herramientas
# como temporizadores mientras el servidor está activo.

cerebros = {}


def obtener_cerebro(uid):
    """
    Obtiene el Cerebro del usuario.

    Si todavía no existe, crea uno nuevo.
    Si ya existe, reutiliza el mismo.
    """

    if uid not in cerebros:
        print(">>> CREANDO NUEVO CEREBRO PARA:", uid)

        cerebros[uid] = Cerebro(uid)

        print(">>> CEREBRO GUARDADO EN MEMORIA")

    else:
        print(">>> REUTILIZANDO CEREBRO EXISTENTE:", uid)

    return cerebros[uid]


# ==================================================
# RUTA PRINCIPAL DE LUMY
# ==================================================

@app.route("/lumy", methods=["POST"])
def lumy():

    try:

        print("\n================================")
        print(">>> NUEVA PETICIÓN A LUMY")
        print("================================")

        # ------------------------------------------
        # RECIBIR DATOS
        # ------------------------------------------

        datos = request.get_json()

        print(">>> DATOS RECIBIDOS:", datos)

        if not datos:
            return jsonify({
                "error": "No se recibieron datos."
            }), 400


        # ------------------------------------------
        # OBTENER UID Y MENSAJE
        # ------------------------------------------

        uid = datos.get("uid")
        mensaje = datos.get("mensaje")

        print(">>> UID:", uid)
        print(">>> MENSAJE:", mensaje)


        # ------------------------------------------
        # VALIDAR UID
        # ------------------------------------------

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400


        # ------------------------------------------
        # VALIDAR MENSAJE
        # ------------------------------------------

        if not mensaje:
            return jsonify({
                "error": "Falta el mensaje."
            }), 400


        # ------------------------------------------
        # OBTENER CEREBRO
        # ------------------------------------------

        print(">>> OBTENIENDO CEREBRO...")

        cerebro = obtener_cerebro(uid)

        print(">>> CEREBRO LISTO")


        # ------------------------------------------
        # PROCESAR MENSAJE
        # ------------------------------------------

        print(">>> PROCESANDO MENSAJE...")

        resultado = cerebro.procesar(mensaje)

        print(">>> RESULTADO GENERADO:")
        print(resultado)


        # ------------------------------------------
        # PROCESAR RESULTADO
        # ------------------------------------------

        if isinstance(resultado, dict):

            respuesta = resultado.get(
                "respuesta",
                ""
            )

            accion = resultado.get(
                "accion",
                None
            )

            requiere_confirmacion = resultado.get(
                "requiere_confirmacion",
                False
            )

        else:

            respuesta = resultado

            accion = None

            requiere_confirmacion = False


        # ------------------------------------------
        # MOSTRAR RESULTADO
        # ------------------------------------------

        print(">>> RESPUESTA:", respuesta)

        print(">>> ACCIÓN:", accion)

        print(
            ">>> REQUIERE CONFIRMACIÓN:",
            requiere_confirmacion
        )


        # ------------------------------------------
        # ENVIAR RESPUESTA A LA WEB
        # ------------------------------------------

        print(">>> ENVIANDO RESPUESTA A LA WEB")


        return jsonify({

            "respuesta": respuesta,

            "accion": accion,

            "requiere_confirmacion":
                requiere_confirmacion

        })


    # ==================================================
    # MANEJO DE ERRORES
    # ==================================================

    except Exception as error:

        print("\n================================")
        print("ERROR EN LUMY:")
        print(error)
        print("================================")


        return jsonify({

            "error": str(error)

        }), 500


# ==================================================
# INICIAR SERVIDOR
# ==================================================

if __name__ == "__main__":

    print("================================")
    print("       LUMY - API")
    print("================================")

    print("Servidor iniciado.")

    print("Esperando conexiones...")

    print("================================")


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
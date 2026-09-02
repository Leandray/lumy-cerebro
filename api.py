from flask import Flask, request, jsonify
from flask_cors import CORS
from cerebro import Cerebro


# ==========================================
# CREAR SERVIDOR
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# RUTA PRINCIPAL DE LUMY
# ==========================================

@app.route("/lumy", methods=["POST"])
def lumy():

    try:

        print("\n================================")
        print(">>> NUEVA PETICIÓN A LUMY")
        print("================================")

        # --------------------------------------
        # RECIBIR DATOS
        # --------------------------------------

        datos = request.get_json()

        print(">>> DATOS RECIBIDOS:", datos)

        if not datos:
            return jsonify({
                "error": "No se recibieron datos."
            }), 400

        uid = datos.get("uid")
        mensaje = datos.get("mensaje")

        print(">>> UID:", uid)
        print(">>> MENSAJE:", mensaje)

        # --------------------------------------
        # COMPROBAR UID
        # --------------------------------------

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400

        # --------------------------------------
        # COMPROBAR MENSAJE
        # --------------------------------------

        if not mensaje:
            return jsonify({
                "error": "Falta el mensaje."
            }), 400

        # --------------------------------------
        # CREAR CEREBRO
        # --------------------------------------

        print(">>> CREANDO CEREBRO...")

        cerebro = Cerebro(uid)

        print(">>> CEREBRO CREADO")

        # --------------------------------------
        # PROCESAR MENSAJE
        # --------------------------------------

        print(">>> PROCESANDO MENSAJE...")

        resultado = cerebro.procesar(mensaje)

        print(">>> RESULTADO GENERADO:")
        print(resultado)

        # --------------------------------------
        # COMPROBAR RESULTADO
        # --------------------------------------

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

        # --------------------------------------
        # MOSTRAR INFORMACIÓN
        # --------------------------------------

        print(">>> RESPUESTA:", respuesta)
        print(">>> ACCIÓN:", accion)
        print(
            ">>> REQUIERE CONFIRMACIÓN:",
            requiere_confirmacion
        )

        # --------------------------------------
        # DEVOLVER RESPUESTA
        # --------------------------------------

        print(">>> ENVIANDO RESPUESTA A LA WEB")

        return jsonify({
            "respuesta": respuesta,
            "accion": accion,
            "requiere_confirmacion": requiere_confirmacion
        })

    except Exception as error:

        print("\n================================")
        print("ERROR EN LUMY:")
        print(error)
        print("================================")

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# INICIAR SERVIDOR
# ==========================================

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
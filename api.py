from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from cerebro import Cerebro
from traductor_guarani import traducir

from oauth_google import (
    construir_url_autorizacion,
    obtener_state,
    intercambiar_code,
    guardar_oauth
)

import os
import hmac


app = Flask(__name__)

CORS(app)


# ==================================================
# CEREBROS ACTIVOS
# ==================================================

# Un Cerebro por usuario.
#
# Esto permite conservar:
# - temporizadores
# - estado emocional
# - personalidad
# - herramientas
#
# mientras el servidor permanezca encendido.

cerebros = {}


# ==================================================
# NOTIFICACIONES
# ==================================================

# Las notificaciones quedan almacenadas
# temporalmente hasta que la web las consulte.

notificaciones = {}

# ==================================================
# COLA DE VOZ PARA LA RASPBERRY PI
# ==================================================

voces_pendientes = {}


# ==================================================
# RECIBIR NOTIFICACIÓN
# ==================================================

def recibir_notificacion(uid, notificacion):

    if uid not in notificaciones:

        notificaciones[uid] = []

    notificaciones[uid].append(
        notificacion
    )

    print(
        ">>> NOTIFICACIÓN GUARDADA PARA:",
        uid
    )


# ==================================================
# OBTENER CEREBRO
# ==================================================

def obtener_cerebro(uid):

    if uid not in cerebros:

        print(
            ">>> CREANDO NUEVO CEREBRO PARA:",
            uid
        )

        cerebros[uid] = Cerebro(
            uid,
            notificar=recibir_notificacion
        )

        print(
            ">>> CEREBRO GUARDADO EN MEMORIA"
        )

    else:

        print(
            ">>> REUTILIZANDO CEREBRO EXISTENTE:",
            uid
        )

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

        datos = request.get_json()

        print(
            ">>> DATOS RECIBIDOS:",
            datos
        )

        if not datos:

            return jsonify({
                "error": "No se recibieron datos."
            }), 400

        # ------------------------------------------
        # UID
        # ------------------------------------------

        uid = datos.get("uid")

        # ------------------------------------------
        # MENSAJE
        # ------------------------------------------

        mensaje = datos.get("mensaje")

        print(
            ">>> UID:",
            uid
        )

        print(
            ">>> MENSAJE:",
            mensaje
        )

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

        print(
            ">>> OBTENIENDO CEREBRO..."
        )

        cerebro = obtener_cerebro(uid)

        print(
            ">>> CEREBRO LISTO"
        )

        # ------------------------------------------
        # PROCESAR
        # ------------------------------------------

        print(
            ">>> PROCESANDO MENSAJE..."
        )

        resultado = cerebro.procesar(
            mensaje
        )

        print(
            ">>> RESULTADO GENERADO:"
        )

        print(
            resultado
        )

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

        print(
            ">>> RESPUESTA:",
            respuesta
        )

        print(
            ">>> ACCIÓN:",
            accion
        )

        print(
            ">>> REQUIERE CONFIRMACIÓN:",
            requiere_confirmacion
        )

        print(
            ">>> ENVIANDO RESPUESTA A LA WEB"
        )

                # ------------------------------------------
        # ENVIAR RESPUESTA A LA COLA DE VOZ
        # ------------------------------------------

        if isinstance(respuesta, str) and respuesta.strip():

            cola = voces_pendientes.setdefault(uid, [])

            cola.append(respuesta.strip())

            # Evitar que la cola crezca indefinidamente.
            if len(cola) > 20:
                del cola[:-20]

            print(
                ">>> RESPUESTA AÑADIDA A LA COLA DE VOZ",
                flush=True
            )

        # ------------------------------------------
        # RESPONDER
        # ------------------------------------------

        return jsonify({

            "respuesta": respuesta,

            "accion": accion,

            "requiere_confirmacion":
                requiere_confirmacion

        })

    except Exception as error:

        print("\n================================")

        print(
            "ERROR EN LUMY:"
        )

        print(
            error
        )

        print(
            "================================"
        )

        return jsonify({

            "error": str(error)

        }), 500

# ==================================================
# COLA DE VOZ - RASPBERRY PI
# ==================================================

@app.route("/voz/pendientes", methods=["GET"])
def obtener_voces_pendientes():

    token_configurado = os.environ.get("LUMY_VOICE_TOKEN", "")
    autorizacion = request.headers.get("Authorization", "")

    if not token_configurado:
        return jsonify({
            "error": "Canal de voz no configurado."
        }), 503

    token_recibido = autorizacion.removeprefix("Bearer ").strip()

    if not hmac.compare_digest(token_recibido, token_configurado):
        return jsonify({
            "error": "No autorizado."
        }), 401

    uid = request.args.get("uid", "").strip()

    if not uid:
        return jsonify({
            "error": "Falta el UID."
        }), 400

    pendientes = voces_pendientes.pop(uid, [])

    return jsonify({
        "mensajes": pendientes
    }), 200

# ==================================================
# OBTENER NOTIFICACIONES
# ==================================================

@app.route(
    "/notificaciones/<uid>",
    methods=["GET"]
)
def obtener_notificaciones(uid):

    try:

        pendientes = notificaciones.get(
            uid,
            []
        )

        # ------------------------------------------
        # ENTREGAR NOTIFICACIONES
        # ------------------------------------------

        notificaciones[uid] = []

        print(
            ">>> NOTIFICACIONES ENVIADAS A:",
            uid
        )

        print(
            ">>> CANTIDAD:",
            len(pendientes)
        )

        return jsonify({

            "notificaciones":
                pendientes

        })

    except Exception as error:

        print(
            ">>> ERROR OBTENIENDO NOTIFICACIONES:",
            error
        )

        return jsonify({

            "error": str(error)

        }), 500


# ============================================================
# GOOGLE OAUTH - YOUTUBE
# ============================================================

@app.route("/oauth/youtube/start", methods=["GET"])
def oauth_youtube_start():
    try:
        uid = request.args.get("uid")

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400

        url = construir_url_autorizacion(
            uid,
            "youtube"
        )

        return redirect(url)

    except Exception as error:
        print("❌ ERROR INICIANDO OAUTH YOUTUBE:")
        print(error)

        return jsonify({
            "error": str(error)
        }), 500


@app.route("/oauth/youtube/callback", methods=["GET"])
def oauth_youtube_callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        error = request.args.get("error")

        if error:
            print(
                "❌ Google rechazó OAuth YouTube:",
                error
            )

            return redirect(
                "https://lumy-c1805.web.app/index.html"
                "?youtube_error="
                + error
            )

        if not code:
            return "❌ No se recibió authorization code.", 400

        datos_state = obtener_state(
            state,
            "youtube"
        )

        if not datos_state:
            return "❌ State OAuth inválido o expirado.", 400

        uid = datos_state["uid"]

        tokens = intercambiar_code(
            code,
            "https://lumy-cerebro.onrender.com/oauth/youtube/callback"
        )

        guardar_oauth(
            uid,
            "youtube",
            tokens
        )

        print(
            "✅ YouTube conectado correctamente:",
            uid
        )

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?youtube_connected=true"
        )

    except Exception as error:
        print("❌ ERROR EN CALLBACK YOUTUBE:")
        print(error)

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?youtube_error=true"
        )


# ============================================================
# GOOGLE OAUTH - CALENDAR
# ============================================================

@app.route("/oauth/calendar/start", methods=["GET"])
def oauth_calendar_start():
    try:
        uid = request.args.get("uid")

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400

        url = construir_url_autorizacion(
            uid,
            "calendar"
        )

        return redirect(url)

    except Exception as error:
        print("❌ ERROR INICIANDO OAUTH CALENDAR:")
        print(error)

        return jsonify({
            "error": str(error)
        }), 500


@app.route("/oauth/calendar/callback", methods=["GET"])
def oauth_calendar_callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        error = request.args.get("error")

        if error:
            print(
                "❌ Google rechazó OAuth Calendar:",
                error
            )

            return redirect(
                "https://lumy-c1805.web.app/index.html"
                "?calendar_error="
                + error
            )

        if not code:
            return "❌ No se recibió authorization code.", 400

        datos_state = obtener_state(
            state,
            "calendar"
        )

        if not datos_state:
            return "❌ State OAuth inválido o expirado.", 400

        uid = datos_state["uid"]

        tokens = intercambiar_code(
            code,
            "https://lumy-cerebro.onrender.com/oauth/calendar/callback"
        )

        guardar_oauth(
            uid,
            "calendar",
            tokens
        )

        print(
            "✅ Google Calendar conectado correctamente:",
            uid
        )

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?calendar_connected=true"
        )

    except Exception as error:
        print("❌ ERROR EN CALLBACK CALENDAR:")
        print(error)

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?calendar_error=true"
        )

# ==================================================
# INICIAR SERVIDOR
# ==================================================

print("\n========== RUTAS DE LUMY ==========")

for ruta in app.url_map.iter_rules():
    print(ruta)

print("===================================\n")

# ============================================================
# OBTENER ACCESS TOKEN VÁLIDO DE YOUTUBE
# ============================================================

@app.route("/oauth/youtube/token", methods=["GET"])
def obtener_token_youtube():
    try:
        uid = request.args.get("uid")

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400

        from oauth_google import obtener_access_token

        token = obtener_access_token(
            uid,
            "youtube"
        )

        return jsonify({
            "access_token": token
        })

    except Exception as error:
        print("❌ ERROR OBTENIENDO TOKEN DE YOUTUBE:")
        print(error)

        return jsonify({
            "error": str(error)
        }), 401
        
@app.route("/oauth/calendar/token", methods=["GET"])
def obtener_token_calendar():
    try:
        uid = request.args.get("uid")

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400

        from oauth_google import obtener_access_token

        token = obtener_access_token(
            uid,
            "calendar"
        )

        return jsonify({
            "access_token": token
        }), 200

    except Exception as error:
        app.logger.exception(
            "ERROR OBTENIENDO TOKEN DE GOOGLE CALENDAR"
        )

        return jsonify({
            "error": str(error)
        }), 401


@app.route("/contacto", methods=["POST"])
def enviar_contacto():
    datos = request.get_json(silent=True) or {}

    nombre = str(datos.get("name", "")).strip()
    correo = str(datos.get("email", "")).strip()
    mensaje = str(datos.get("message", "")).strip()

    if not nombre or not correo or not mensaje:
        return jsonify({
            "error": "Completa todos los campos."
        }), 400

    if (
        len(nombre) > 100
        or len(correo) > 254
        or len(mensaje) > 5000
    ):
        return jsonify({
            "error": "El mensaje supera el límite permitido."
        }), 400

    api_key = os.environ.get("RESEND_API_KEY")
    correo_admin = os.environ.get("CONTACT_EMAIL")
    remitente = os.environ.get("RESEND_FROM")

    if not api_key or not correo_admin or not remitente:
        app.logger.error(
            "Falta configurar el servicio de correo."
        )

        return jsonify({
            "error": "Servicio de correo no configurado."
        }), 500

    contenido = (
        "Nuevo mensaje desde el formulario de contacto de LUMY\n\n"
        f"Nombre: {nombre}\n"
        f"Correo del remitente: {correo}\n\n"
        f"Mensaje:\n{mensaje}"
    )

    try:
        respuesta = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": remitente,
                "to": [correo_admin],
                "reply_to": correo,
                "subject": f"Nuevo mensaje de contacto de LUMY: {nombre}",
                "text": contenido,
            },
            timeout=20,
        )

        if not respuesta.ok:
            app.logger.error(
                "Falló el envío de contacto. HTTP %s",
                respuesta.status_code,
            )

            return jsonify({
                "error": "No se pudo enviar el correo."
            }), 502

        return jsonify({
            "ok": True,
            "message": "Correo enviado."
        }), 200

    except requests.RequestException:
        app.logger.exception(
            "Error de conexión con el servicio de correo."
        )

        return jsonify({
            "error": "No se pudo conectar con el servicio de correo."
        }), 502


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
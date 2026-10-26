
import hmac
import logging
import os

import requests
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

from cerebro import Cerebro
from oauth_google import (
    construir_url_autorizacion,
    obtener_state,
    intercambiar_code,
    guardar_oauth,
)

app = Flask(__name__)
CORS(app)

# ==========================================
# CEREBROS ACTIVOS
# ==========================================

cerebros = {}

# ==========================================
# NOTIFICACIONES Y COLA DE VOZ
# ==========================================

notificaciones = {}
voces_pendientes = {}


def recibir_notificacion(uid, notificacion):
    notificaciones.setdefault(uid, []).append(notificacion)


# ==========================================
# OBTENER CEREBRO
# ==========================================

def obtener_cerebro(uid):
    if uid not in cerebros:
        print(
            ">>> CREANDO NUEVO CEREBRO PARA:",
            uid,
            flush=True,
        )

        nuevo_cerebro = Cerebro(
            uid,
            notificar=recibir_notificacion,
        )

        cerebros[uid] = nuevo_cerebro

        print(
            ">>> CEREBRO GUARDADO EN MEMORIA",
            flush=True,
        )
    else:
        print(
            ">>> REUTILIZANDO CEREBRO EXISTENTE:",
            uid,
            flush=True,
        )

    return cerebros[uid]


# ==========================================
# RUTA PRINCIPAL DE LUMY
# ==========================================

@app.route("/lumy", methods=["POST"])
def lumy():
    try:
        print("\n================================", flush=True)
        print(">>> NUEVA PETICIÓN A LUMY", flush=True)
        print("================================", flush=True)

        datos = request.get_json(silent=True)

        print(">>> DATOS RECIBIDOS:", datos, flush=True)

        if not isinstance(datos, dict):
            return jsonify({
                "error": "No se recibieron datos JSON válidos."
            }), 400

        uid = datos.get("uid")
        mensaje = datos.get("mensaje")

        print(">>> UID:", uid, flush=True)
        print(">>> MENSAJE:", mensaje, flush=True)

        if not uid:
            return jsonify({
                "error": "Falta el UID del usuario."
            }), 400

        if not isinstance(mensaje, str) or not mensaje.strip():
            return jsonify({
                "error": "Falta el mensaje."
            }), 400

        print(">>> OBTENIENDO CEREBRO...", flush=True)

        cerebro = obtener_cerebro(uid)

        print(">>> CEREBRO LISTO", flush=True)
        print(">>> PROCESANDO MENSAJE...", flush=True)

        resultado = cerebro.procesar(mensaje.strip())

        print(">>> RESULTADO GENERADO:", flush=True)
        print(resultado, flush=True)

        if isinstance(resultado, dict):
            respuesta = resultado.get("respuesta", "")
            accion = resultado.get("accion")
            requiere_confirmacion = resultado.get(
                "requiere_confirmacion",
                False,
            )
        else:
            respuesta = resultado
            accion = None
            requiere_confirmacion = False

        print(">>> RESPUESTA:", respuesta, flush=True)
        print(">>> ACCIÓN:", accion, flush=True)
        print(
            ">>> REQUIERE CONFIRMACIÓN:",
            requiere_confirmacion,
            flush=True,
        )

        # ==========================================
        # COLA DE VOZ PARA RASPBERRY PI
        # ==========================================

        if isinstance(respuesta, str) and respuesta.strip():
            cola = voces_pendientes.setdefault(uid, [])
            cola.append(respuesta.strip())

            if len(cola) > 20:
                del cola[:-20]

            print(
                ">>> RESPUESTA AÑADIDA A LA COLA DE VOZ",
                flush=True,
            )

        # ==========================================
        # RESPUESTA A LA WEB
        # ==========================================

        return jsonify({
            "respuesta": respuesta,
            "accion": accion,
            "requiere_confirmacion": requiere_confirmacion,
        }), 200

    except Exception as error:
        app.logger.exception(
            "TRAZA COMPLETA DEL ERROR EN LUMY"
        )

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# COLA DE VOZ - RASPBERRY PI
# ==========================================

@app.route("/voz/pendientes", methods=["GET"])
def obtener_voces_pendientes():
    token_configurado = os.environ.get(
        "LUMY_VOICE_TOKEN",
        "",
    )

    autorizacion = request.headers.get(
        "Authorization",
        "",
    )

    if not token_configurado:
        return jsonify({
            "error": "Canal de voz no configurado."
        }), 503

    token_recibido = autorizacion.removeprefix(
        "Bearer "
    ).strip()

    if not hmac.compare_digest(
        token_recibido,
        token_configurado,
    ):
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


# ==========================================
# OBTENER NOTIFICACIONES
# ==========================================

@app.route("/notificaciones/<uid>", methods=["GET"])
def obtener_notificaciones(uid):
    try:
        pendientes = notificaciones.get(uid, [])
        notificaciones[uid] = []

        print(
            ">>> NOTIFICACIONES ENVIADAS A:",
            uid,
            flush=True,
        )

        print(
            ">>> CANTIDAD:",
            len(pendientes),
            flush=True,
        )

        return jsonify({
            "notificaciones": pendientes
        }), 200

    except Exception:
        app.logger.exception(
            "ERROR OBTENIENDO NOTIFICACIONES"
        )

        return jsonify({
            "error": "No se pudieron obtener las notificaciones."
        }), 500


# ==========================================
# GOOGLE OAUTH - YOUTUBE
# ==========================================

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
            "youtube",
        )

        return redirect(url)

    except Exception:
        app.logger.exception(
            "ERROR INICIANDO OAUTH YOUTUBE"
        )

        return jsonify({
            "error": "No se pudo iniciar OAuth de YouTube."
        }), 500


@app.route("/oauth/youtube/callback", methods=["GET"])
def oauth_youtube_callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        error_oauth = request.args.get("error")

        if error_oauth:
            logging.error(
                "Google rechazó OAuth YouTube: %s",
                error_oauth,
            )

            return redirect(
                "https://lumy-c1805.web.app/index.html"
                "?youtube_error="
                + error_oauth
            )

        if not code:
            return "No se recibió authorization code.", 400

        datos_state = obtener_state(
            state,
            "youtube",
        )

        if not datos_state:
            return "State OAuth inválido o expirado.", 400

        uid = datos_state["uid"]

        tokens = intercambiar_code(
            code,
            "https://lumy-cerebro.onrender.com/oauth/youtube/callback",
        )

        guardar_oauth(
            uid,
            "youtube",
            tokens,
        )

        print(
            "YouTube conectado correctamente:",
            uid,
            flush=True,
        )

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?youtube_connected=true"
        )

    except Exception:
        app.logger.exception(
            "ERROR EN CALLBACK YOUTUBE"
        )

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?youtube_error=true"
        )


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
            "youtube",
        )

        return jsonify({
            "access_token": token
        }), 200

    except Exception:
        app.logger.exception(
            "ERROR OBTENIENDO TOKEN DE YOUTUBE"
        )

        return jsonify({
            "error": "No se pudo obtener el token de YouTube."
        }), 401


# ==========================================
# GOOGLE OAUTH - CALENDAR
# ==========================================

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
            "calendar",
        )

        return redirect(url)

    except Exception:
        app.logger.exception(
            "ERROR INICIANDO OAUTH CALENDAR"
        )

        return jsonify({
            "error": "No se pudo iniciar OAuth de Calendar."
        }), 500


@app.route("/oauth/calendar/callback", methods=["GET"])
def oauth_calendar_callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        error_oauth = request.args.get("error")

        if error_oauth:
            logging.error(
                "Google rechazó OAuth Calendar: %s",
                error_oauth,
            )

            return redirect(
                "https://lumy-c1805.web.app/index.html"
                "?calendar_error="
                + error_oauth
            )

        if not code:
            return "No se recibió authorization code.", 400

        datos_state = obtener_state(
            state,
            "calendar",
        )

        if not datos_state:
            return "State OAuth inválido o expirado.", 400

        uid = datos_state["uid"]

        tokens = intercambiar_code(
            code,
            "https://lumy-cerebro.onrender.com/oauth/calendar/callback",
        )

        guardar_oauth(
            uid,
            "calendar",
            tokens,
        )

        print(
            "Google Calendar conectado correctamente:",
            uid,
            flush=True,
        )

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?calendar_connected=true"
        )

    except Exception:
        app.logger.exception(
            "ERROR EN CALLBACK CALENDAR"
        )

        return redirect(
            "https://lumy-c1805.web.app/index.html"
            "?calendar_error=true"
        )


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
            "calendar",
        )

        return jsonify({
            "access_token": token
        }), 200

    except Exception:
        app.logger.exception(
            "ERROR OBTENIENDO TOKEN DE GOOGLE CALENDAR"
        )

        return jsonify({
            "error": "No se pudo obtener el token de Calendar."
        }), 401


# ==========================================
# FORMULARIO DE CONTACTO
# ==========================================

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


# ==========================================
# MOSTRAR RUTAS
# ==========================================

print("\n========== RUTAS DE LUMY ==========")

for ruta in app.url_map.iter_rules():
    print(ruta)

print("===================================\n")


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":
    print("================================")
    print("       LUMY - API")
    print("================================")
    print("Servidor iniciado.")
    print("Esperando conexiones...")
    print("===============================")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
    )
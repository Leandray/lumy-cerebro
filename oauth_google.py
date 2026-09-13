import os
import secrets
import time

import requests

from firebase.firebase import db


# ============================================================
# CONFIGURACIÓN
# ============================================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

FRONTEND_URL = "https://lumy-c1805.web.app"


# Estados OAuth temporales.
# state -> {"uid": "...", "servicio": "...", "creado": timestamp}
oauth_states = {}


# ============================================================
# SCOPES
# ============================================================

YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly"
]

CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]


# ============================================================
# REDIRECT URIS
# ============================================================

YOUTUBE_REDIRECT_URI = (
    "https://lumy-cerebro.onrender.com/oauth/youtube/callback"
)

CALENDAR_REDIRECT_URI = (
    "https://lumy-cerebro.onrender.com/oauth/calendar/callback"
)


# ============================================================
# CREAR STATE
# ============================================================

def crear_state(uid, servicio):
    state = secrets.token_urlsafe(32)

    oauth_states[state] = {
        "uid": uid,
        "servicio": servicio,
        "creado": time.time()
    }

    return state


# ============================================================
# OBTENER Y VALIDAR STATE
# ============================================================

def obtener_state(state, servicio):
    if not state:
        return None

    datos = oauth_states.get(state)

    if not datos:
        return None

    # El state solamente es válido durante 10 minutos.
    if time.time() - datos["creado"] > 600:
        oauth_states.pop(state, None)
        return None

    if datos["servicio"] != servicio:
        return None

    # El state solamente puede utilizarse una vez.
    oauth_states.pop(state, None)

    return datos


# ============================================================
# CONSTRUIR URL DE GOOGLE
# ============================================================

def construir_url_autorizacion(
    uid,
    servicio
):
    if servicio == "youtube":
        scopes = YOUTUBE_SCOPES
        redirect_uri = YOUTUBE_REDIRECT_URI

    elif servicio == "calendar":
        scopes = CALENDAR_SCOPES
        redirect_uri = CALENDAR_REDIRECT_URI

    else:
        raise ValueError("Servicio OAuth no válido.")

    state = crear_state(uid, servicio)

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }

    from urllib.parse import urlencode

    url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode(params)
    )

    return url


# ============================================================
# INTERCAMBIAR CODE POR TOKENS
# ============================================================

def intercambiar_code(code, redirect_uri):
    datos = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    respuesta = requests.post(
        GOOGLE_TOKEN_URL,
        data=datos,
        timeout=30
    )

    if not respuesta.ok:
        print(
            "❌ Error intercambiando authorization code:"
        )
        print(respuesta.text)

        raise Exception(
            "No se pudo obtener el token de Google."
        )

    return respuesta.json()


# ============================================================
# GUARDAR OAUTH EN FIRESTORE
# ============================================================

def guardar_oauth(
    uid,
    servicio,
    tokens
):
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in", 3600)

    if not access_token:
        raise Exception(
            "Google no devolvió access_token."
        )

    datos = {
        "access_token": access_token,
        "expires_at": int(time.time()) + int(expires_in)
    }

    # Google puede no enviar refresh_token
    # en todas las renovaciones.
    #
    # Si ya existe uno, no debemos sobrescribirlo
    # con None.
    if refresh_token:
        datos["refresh_token"] = refresh_token

    campo = f"{servicio}_oauth"

    db.collection("users").document(uid).set(
        {
            campo: datos
        },
        merge=True
    )

    print(
        f"✅ OAuth de {servicio} guardado para:",
        uid
    )


# ============================================================
# OBTENER OAUTH
# ============================================================

def obtener_oauth(uid, servicio):
    documento = (
        db.collection("users")
        .document(uid)
        .get()
    )

    if not documento.exists:
        return None

    datos = documento.to_dict()

    return datos.get(
        f"{servicio}_oauth"
    )


# ============================================================
# RENOVAR ACCESS TOKEN
# ============================================================

def renovar_access_token(
    uid,
    servicio
):
    oauth = obtener_oauth(
        uid,
        servicio
    )

    if not oauth:
        raise Exception(
            f"{servicio.upper()}_NO_CONECTADO"
        )

    refresh_token = oauth.get(
        "refresh_token"
    )

    if not refresh_token:
        raise Exception(
            f"{servicio.upper()}_SIN_REFRESH_TOKEN"
        )

    datos = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    respuesta = requests.post(
        GOOGLE_TOKEN_URL,
        data=datos,
        timeout=30
    )

    if not respuesta.ok:
        print(
            "❌ Error renovando token:",
            respuesta.text
        )

        raise Exception(
            f"{servicio.upper()}_REFRESH_ERROR"
        )

    tokens = respuesta.json()

    nuevo_access_token = tokens.get(
        "access_token"
    )

    expires_in = tokens.get(
        "expires_in",
        3600
    )

    if not nuevo_access_token:
        raise Exception(
            "Google no devolvió un nuevo access_token."
        )

    campo = f"{servicio}_oauth"

    db.collection("users").document(uid).set(
        {
            campo: {
                "access_token": nuevo_access_token,
                "expires_at": int(time.time())
                + int(expires_in)
            }
        },
        merge=True
    )

    print(
        f"🔄 Access token renovado: {servicio}"
    )

    return nuevo_access_token


# ============================================================
# OBTENER ACCESS TOKEN VÁLIDO
# ============================================================

def obtener_access_token(
    uid,
    servicio
):
    oauth = obtener_oauth(
        uid,
        servicio
    )

    if not oauth:
        raise Exception(
            f"{servicio.upper()}_NO_CONECTADO"
        )

    access_token = oauth.get(
        "access_token"
    )

    expires_at = oauth.get(
        "expires_at",
        0
    )

    # Renovamos 5 minutos antes de que expire.
    margen = 300

    if (
        access_token
        and time.time() < expires_at - margen
    ):
        return access_token

    return renovar_access_token(
        uid,
        servicio
    )
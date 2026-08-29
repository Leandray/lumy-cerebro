import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path
import os


# ==========================================
# UBICACIÓN DE LAS CREDENCIALES
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

CREDENTIALS_FILE = (
    BASE_DIR
    / "CREDENCIALES"
    / "lumy-c1805-firebase-adminsdk-fbsvc-10d22b066c.json"
)


# ==========================================
# INICIALIZAR FIREBASE
# ==========================================

if not firebase_admin._apps:

    # --------------------------------------
    # RENDER / PRODUCCIÓN
    # --------------------------------------

    RENDER_CREDENTIALS = Path(
        "/etc/secrets/lumy-firebase-adminsdk.json"
    )

    if RENDER_CREDENTIALS.exists():

        cred = credentials.Certificate(
            str(RENDER_CREDENTIALS)
        )

        print("🔥 Firebase: usando credenciales de Render.")

    # --------------------------------------
    # DESARROLLO LOCAL
    # --------------------------------------

    elif CREDENTIALS_FILE.exists():

        cred = credentials.Certificate(
            str(CREDENTIALS_FILE)
        )

        print("🔥 Firebase: usando credenciales locales.")

    # --------------------------------------
    # NO ENCONTRADAS
    # --------------------------------------

    else:

        raise FileNotFoundError(
            "No se encontraron las credenciales de Firebase."
        )


    # --------------------------------------
    # INICIAR FIREBASE
    # --------------------------------------

    firebase_admin.initialize_app(cred)


# ==========================================
# FIRESTORE
# ==========================================

db = firestore.client()
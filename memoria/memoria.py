
import logging

from memoria.memoria_firebase import FirebaseMemoria


class Memoria:
    def __init__(self, uid):
        self.uid = uid

        self.usuario = {
            "nombre": "",
            "pronombres": "",
        }
        self.preferencias = {}
        self.configuracion = {}
        self.recuerdos = []
        self.conversacion = []

        self.firebase = None

        try:
            firebase = FirebaseMemoria(uid)

            identidad = firebase.cargar_identidad() or {}
            memoria = firebase.cargar_memoria() or {}

            if not isinstance(identidad, dict):
                identidad = {}
            if not isinstance(memoria, dict):
                memoria = {}

            self.usuario["nombre"] = identidad.get("nombre", "")
            self.usuario["pronombres"] = identidad.get("pronombres", "")

            self.conversacion = memoria.get("conversacion", [])
            self.preferencias = memoria.get("preferencias", {})
            self.configuracion = memoria.get("configuracion", {})
            self.recuerdos = memoria.get("recuerdos", [])

            if not isinstance(self.conversacion, list):
                self.conversacion = []
            if not isinstance(self.preferencias, dict):
                self.preferencias = {}
            if not isinstance(self.configuracion, dict):
                self.configuracion = {}
            if not isinstance(self.recuerdos, list):
                self.recuerdos = []

            self.firebase = firebase
            print("[MEMORIA] Firebase cargado correctamente.", flush=True)

        except Exception:
            logging.exception(
                "[MEMORIA] No se pudo cargar Firebase. "
                "LUMY continuará con memoria temporal."
            )
            self.firebase = None

    def establecer_usuario(self, nombre=None, pronombres=None):
        if nombre is not None:
            nombre = str(nombre).strip()
            if nombre:
                self.usuario["nombre"] = nombre

        if pronombres is not None:
            pronombres = str(pronombres).strip()
            if pronombres:
                self.usuario["pronombres"] = pronombres

        if self.firebase is not None:
            try:
                self.firebase.guardar_identidad(
                    nombre=self.usuario["nombre"],
                    pronombres=self.usuario["pronombres"],
                )
            except Exception:
                logging.exception(
                    "[MEMORIA] No se pudo guardar la identidad."
                )

    def obtener_usuario(self):
        return self.usuario.copy()

    def guardar_preferencia(self, clave, valor):
        self.preferencias[clave] = valor
        self.guardar_memoria()

    def obtener_preferencia(self, clave):
        return self.preferencias.get(clave)

    def guardar_configuracion(self, clave, valor):
        self.configuracion[clave] = valor
        self.guardar_memoria()

    def obtener_configuracion(self, clave):
        return self.configuracion.get(clave)

    def guardar_recuerdo(self, recuerdo):
        if not recuerdo:
            return

        recuerdo = str(recuerdo).strip()

        if recuerdo and recuerdo not in self.recuerdos:
            self.recuerdos.append(recuerdo)
            self.guardar_memoria()

    def obtener_recuerdos(self):
        return self.recuerdos.copy()

    def obtener_contexto(self):
        return {
            "usuario": self.usuario.copy(),
            "preferencias": self.preferencias.copy(),
            "configuracion": self.configuracion.copy(),
            "recuerdos": self.recuerdos.copy(),
        }

    def obtener_contexto_relevante(
        self, mensaje, limite_recuerdos=8, limite_conversacion=6
    ):
        mensaje = str(mensaje or "").lower().strip()
        palabras_mensaje = set(mensaje.split())

        recuerdos_relevantes = []

        for recuerdo in self.recuerdos:
            if not isinstance(recuerdo, str):
                continue

            palabras_recuerdo = set(recuerdo.lower().split())

            if palabras_mensaje & palabras_recuerdo:
                recuerdos_relevantes.append(recuerdo)

        if not recuerdos_relevantes:
            recuerdos_relevantes = self.recuerdos[-limite_recuerdos:]
        else:
            recuerdos_relevantes = recuerdos_relevantes[-limite_recuerdos:]

        conversacion_reciente = self.conversacion[-limite_conversacion:]

        return {
            "usuario": self.usuario.copy(),
            "preferencias": self.preferencias.copy(),
            "configuracion": self.configuracion.copy(),
            "recuerdos": recuerdos_relevantes,
            "conversacion": conversacion_reciente,
        }

    def guardar_mensaje(self, usuario, lumy):
        self.conversacion.append({
            "usuario": usuario,
            "lumy": lumy,
        })

        self.conversacion = self.conversacion[-20:]
        self.guardar_memoria()

    def obtener_conversacion(self):
        return self.conversacion.copy()

    def guardar_memoria(self):
        if self.firebase is None:
            print(
                "[MEMORIA] Firebase no disponible; cambios conservados "
                "solo en memoria temporal.",
                flush=True,
            )
            return

        try:
            self.firebase.guardar_memoria({
                "conversacion": self.conversacion,
                "preferencias": self.preferencias,
                "configuracion": self.configuracion,
                "recuerdos": self.recuerdos,
            })
        except Exception:
            logging.exception(
                "[MEMORIA] No se pudo guardar la memoria en Firebase."
            )

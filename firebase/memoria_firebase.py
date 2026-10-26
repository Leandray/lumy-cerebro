
from firebase.firebase import db


class FirebaseMemoria:
    def __init__(self, uid):
        self.uid = uid
        self.usuario_ref = db.collection("users").document(uid)

    def cargar_memoria(self):
        documento = self.usuario_ref.get()

        if not documento.exists:
            return {}

        datos = documento.to_dict() or {}
        memoria = datos.get("memory", {})

        if not isinstance(memoria, dict):
            return {}

        return memoria

    def guardar_memoria(self, memoria):
        self.usuario_ref.set(
            {"memory": memoria},
            merge=True,
        )

    def guardar_identidad(self, nombre=None, pronombres=None):
        identidad = {}

        if nombre is not None:
            identidad["name"] = nombre

        if pronombres is not None:
            identidad["pronouns"] = pronombres

        if identidad:
            self.usuario_ref.set(
                {"identity": identidad},
                merge=True,
            )

    def cargar_identidad(self):
        documento = self.usuario_ref.get()

        if not documento.exists:
            return {}

        datos = documento.to_dict() or {}
        identidad = datos.get("identity", {})

        if not isinstance(identidad, dict):
            return {}

        return identidad

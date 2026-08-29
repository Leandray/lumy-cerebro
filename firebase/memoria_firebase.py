from firebase.firebase import db


class FirebaseMemoria:

    def __init__(self, uid):
        self.uid = uid

        self.usuario_ref = (
            db.collection("users").document(uid)
        )

    # ==========================================
    # CARGAR MEMORIA
    # ==========================================

    def cargar_memoria(self):

        documento = self.usuario_ref.get()

        if not documento.exists:
            return {}

        datos = documento.to_dict()

        return datos.get("memory", {})

    # ==========================================
    # GUARDAR MEMORIA
    # ==========================================

    def guardar_memoria(self, memoria):

        self.usuario_ref.set(
            {
                "memory": memoria
            },
            merge=True
        )

    # ==========================================
    # GUARDAR IDENTIDAD
    # ==========================================

    def guardar_identidad(
        self,
        nombre=None,
        pronombres=None
    ):

        identidad = {}

        if nombre:
            identidad["name"] = nombre

        if pronombres:
            identidad["pronombres"] = pronombres

        if identidad:

            self.usuario_ref.set(
                {
                    "identity": identidad
                },
                merge=True
            )

    # ==========================================
    # CARGAR IDENTIDAD
    # ==========================================

    def cargar_identidad(self):

        documento = self.usuario_ref.get()

        if not documento.exists:
            return {}

        datos = documento.to_dict()

        return datos.get("identity", {})
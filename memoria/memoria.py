from firebase.memoria_firebase import FirebaseMemoria


class Memoria:

    def __init__(self, uid):
        self.uid = uid

        # ==========================================
        # MEMORIA DEL USUARIO
        # ==========================================

        self.usuario = {
            "nombre": None,
            "pronombres": None
        }

        # ==========================================
        # PREFERENCIAS
        # ==========================================

        self.preferencias = {}

        # ==========================================
        # CONFIGURACIÓN
        # ==========================================

        self.configuracion = {}

        # ==========================================
        # RECUERDOS PERMANENTES
        # ==========================================

        self.recuerdos = []

        # ==========================================
        # MEMORIA TEMPORAL
        # ==========================================

        self.conversacion = []

        # ==========================================
        # CONEXIÓN CON FIREBASE
        # ==========================================

        self.firebase = FirebaseMemoria(uid)

        # ==========================================
        # CARGAR IDENTIDAD
        # ==========================================

        identidad = self.firebase.cargar_identidad()

        if identidad:
            self.usuario["nombre"] = identidad.get("name")
            self.usuario["pronombres"] = identidad.get("pronombres")

        # ==========================================
        # CARGAR MEMORIA
        # ==========================================

        memoria = self.firebase.cargar_memoria()

        if memoria:
            self.conversacion = memoria.get(
                "conversacion",
                []
            )

            self.preferencias = memoria.get(
                "preferencias",
                {}
            )

            self.configuracion = memoria.get(
                "configuracion",
                {}
            )

            self.recuerdos = memoria.get(
                "recuerdos",
                []
            )

    # ==========================================
    # ESTABLECER USUARIO
    # ==========================================

    def establecer_usuario(
        self,
        nombre=None,
        pronombres=None
    ):

        if nombre:
            self.usuario["nombre"] = nombre.strip()

        if pronombres:
            self.usuario["pronombres"] = pronombres.strip()

        # Guardar permanentemente

        self.firebase.guardar_identidad(
            nombre=self.usuario["nombre"],
            pronombres=self.usuario["pronombres"]
        )

    # ==========================================
    # OBTENER USUARIO
    # ==========================================

    def obtener_usuario(self):

        return self.usuario.copy()

    # ==========================================
    # GUARDAR PREFERENCIA
    # ==========================================

    def guardar_preferencia(
        self,
        clave,
        valor
    ):

        self.preferencias[clave] = valor

        self.guardar_memoria()

    # ==========================================
    # OBTENER PREFERENCIA
    # ==========================================

    def obtener_preferencia(self, clave):

        return self.preferencias.get(clave)

    # ==========================================
    # GUARDAR CONFIGURACIÓN
    # ==========================================

    def guardar_configuracion(
        self,
        clave,
        valor
    ):

        self.configuracion[clave] = valor

        self.guardar_memoria()

    # ==========================================
    # OBTENER CONFIGURACIÓN
    # ==========================================

    def obtener_configuracion(self, clave):

        return self.configuracion.get(clave)

    # ==========================================
    # GUARDAR RECUERDO
    # ==========================================

    def guardar_recuerdo(self, recuerdo):

        if not recuerdo:
            return

        recuerdo = recuerdo.strip()

        if recuerdo and recuerdo not in self.recuerdos:

            self.recuerdos.append(recuerdo)

            self.guardar_memoria()

    # ==========================================
    # OBTENER RECUERDOS
    # ==========================================

    def obtener_recuerdos(self):

        return self.recuerdos.copy()

    # ==========================================
    # OBTENER CONTEXTO COMPLETO
    # ==========================================

    def obtener_contexto(self):

        return {
            "usuario": self.usuario.copy(),
            "preferencias": self.preferencias.copy(),
            "configuracion": self.configuracion.copy(),
            "recuerdos": self.recuerdos.copy()
        }

    # ==========================================
    # GUARDAR MENSAJE
    # ==========================================

    def guardar_mensaje(
        self,
        usuario,
        lumy
    ):

        self.conversacion.append({
            "usuario": usuario,
            "lumy": lumy
        })

        self.guardar_memoria()

    # ==========================================
    # OBTENER CONVERSACIÓN
    # ==========================================

    def obtener_conversacion(self):

        return self.conversacion.copy()

    # ==========================================
    # GUARDAR MEMORIA COMPLETA
    # ==========================================

    def guardar_memoria(self):

        self.firebase.guardar_memoria({

            "conversacion": self.conversacion,

            "preferencias": self.preferencias,

            "configuracion": self.configuracion,

            "recuerdos": self.recuerdos

        })
class Emociones:

    def __init__(self):

        self.estados = {
            "felicidad": 0,
            "tristeza": 0,
            "enojo": 0,
            "miedo": 0,
            "sorpresa": 0,
            "curiosidad": 0,
            "energia": 70
        }

    # ==================================================
    # DETERMINAR EMOCIÓN ACTUAL
    # ==================================================

    def emocion_actual(self):

        emociones = {
            "feliz": self.estados["felicidad"],
            "triste": self.estados["tristeza"],
            "enojada": self.estados["enojo"],
            "asustada": self.estados["miedo"],
            "sorprendida": self.estados["sorpresa"],
            "curiosa": self.estados["curiosidad"]
        }

        emocion, valor = max(
            emociones.items(),
            key=lambda x: x[1]
        )

        if valor < 20:
            return "neutral"

        return emocion

    # ==================================================
    # MODIFICAR EMOCIÓN
    # ==================================================

    def modificar(self, emocion, cantidad):

        if emocion not in self.estados:
            return

        self.estados[emocion] += cantidad

        self.estados[emocion] = max(
            0,
            min(100, self.estados[emocion])
        )

    # ==================================================
    # CALMAR EMOCIONES
    # ==================================================

    def calmar(self, cantidad=5):

        emociones = [
            "felicidad",
            "tristeza",
            "enojo",
            "miedo",
            "sorpresa",
            "curiosidad"
        ]

        for emocion in emociones:

            if self.estados[emocion] > 0:

                self.estados[emocion] = max(
                    0,
                    self.estados[emocion] - cantidad
                )

    # ==================================================
    # DETECTAR EMOCIÓN DEL MENSAJE
    # ==================================================

    def detectar(self, mensaje):

        mensaje = mensaje.lower().strip()

        # ----------------------------------------------
        # FELICIDAD
        # ----------------------------------------------

        palabras_felices = [
            "jajaja",
            "jajaja",
            "me encanta",
            "estoy feliz",
            "soy feliz",
            "qué bonito",
            "que bonito",
            "lo logré",
            "lo logre",
            "funcionó",
            "funciono",
            "gracias",
            "me gusta mucho"
        ]

        # ----------------------------------------------
        # TRISTEZA
        # ----------------------------------------------

        palabras_tristes = [
            "estoy triste",
            "me siento triste",
            "me siento mal",
            "estoy mal",
            "estoy solo",
            "estoy sola",
            "llorando",
            "quiero llorar",
            "perdí",
            "perdi",
            "no puedo",
            "estoy preocupado",
            "estoy preocupada",
            "me duele"
        ]

        # ----------------------------------------------
        # ENOJO
        # ----------------------------------------------

        palabras_enojadas = [
            "estoy enojado",
            "estoy enojada",
            "estoy molesto",
            "estoy molesta",
            "qué rabia",
            "que rabia",
            "me da rabia",
            "estoy harto",
            "estoy harta",
            "es injusto",
            "esto es injusto",
            "me hicieron trampa"
        ]

        # ----------------------------------------------
        # MIEDO
        # ----------------------------------------------

        palabras_miedo = [
            "tengo miedo",
            "estoy asustado",
            "estoy asustada",
            "me asusta",
            "me da miedo",
            "estoy aterrorizado",
            "estoy aterrorizada",
            "qué miedo",
            "que miedo"
        ]

        # ----------------------------------------------
        # SORPRESA
        # ----------------------------------------------

        palabras_sorpresa = [
            "wow",
            "guau",
            "no puede ser",
            "no puedo creerlo",
            "increíble",
            "increible",
            "qué sorpresa",
            "que sorpresa",
            "mira lo que pasó",
            "mira lo que paso",
            "acabo de descubrir"
        ]

        # ----------------------------------------------
        # CURIOSIDAD
        # ----------------------------------------------

        palabras_curiosidad = [
            "cómo funciona",
            "como funciona",
            "por qué",
            "por que",
            "cómo se hace",
            "como se hace",
            "qué es",
            "que es",
            "sabías que",
            "sabias que",
            "quiero saber",
            "me pregunto",
            "es interesante",
            "cuéntame",
            "cuentame"
        ]

        # ==================================================
        # APLICAR EMOCIONES
        # ==================================================

        detectada = None

        if any(palabra in mensaje for palabra in palabras_felices):

            self.modificar("felicidad", 20)
            detectada = "feliz"

        elif any(palabra in mensaje for palabra in palabras_tristes):

            self.modificar("tristeza", 25)
            detectada = "triste"

        elif any(palabra in mensaje for palabra in palabras_enojadas):

            self.modificar("enojo", 25)
            detectada = "enojada"

        elif any(palabra in mensaje for palabra in palabras_miedo):

            self.modificar("miedo", 25)
            detectada = "asustada"

        elif any(palabra in mensaje for palabra in palabras_sorpresa):

            self.modificar("sorpresa", 25)
            detectada = "sorprendida"

        elif any(palabra in mensaje for palabra in palabras_curiosidad):

            self.modificar("curiosidad", 20)
            detectada = "curiosa"

        return detectada

    # ==================================================
    # OBTENER ESTADO COMPLETO
    # ==================================================

    def obtener_estado(self):

        return {
            "emocion": self.emocion_actual(),
            "valores": self.estados.copy()
        }
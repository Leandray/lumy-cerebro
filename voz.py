import speech_recognition as sr
import pyttsx3


class Voz:

    def __init__(self):

        # ==========================================
        # RECONOCIMIENTO DE VOZ
        # ==========================================

        self.reconocedor = sr.Recognizer()

        # ==========================================
        # SÍNTESIS DE VOZ
        # ==========================================

        self.motor = pyttsx3.init()

        # Velocidad de habla
        self.motor.setProperty("rate", 165)

        # Volumen
        self.motor.setProperty("volume", 1.0)

    # ==========================================
    # ESCUCHAR
    # ==========================================

    def escuchar(self):

        with sr.Microphone() as fuente:

            print("\n🎤 LUMY está escuchando...")
            print("Habla ahora...")

            self.reconocedor.adjust_for_ambient_noise(
                fuente,
                duration=0.5
            )

            audio = self.reconocedor.listen(fuente)

        try:

            print("🧠 Reconociendo voz...")

            texto = self.reconocedor.recognize_google(
                audio,
                language="es-ES"
            )

            print("👤 Tú:", texto)

            return texto

        except sr.UnknownValueError:

            print("❌ No pude entender lo que dijiste.")
            return None

        except sr.RequestError as error:

            print("❌ Error del reconocimiento de voz:")
            print(error)

            return None

    # ==========================================
    # HABLAR
    # ==========================================

    def hablar(self, texto):

        if not texto:
            return

        print("🔊 LUMY:", texto)

        self.motor.say(texto)
        self.motor.runAndWait()
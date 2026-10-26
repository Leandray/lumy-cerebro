
import os
import uuid
import speech_recognition as sr

try:
    from TTS.api import TTS
except Exception as error:
    TTS = None
    print("[LUMY VOZ] XTTS no está disponible:", error)

try:
    import pygame
except Exception as error:
    pygame = None
    print("[LUMY VOZ] pygame no está disponible:", error)


class Voz:
    def __init__(self):
        self.reconocedor = sr.Recognizer()
        self.tts = None
        self.audio_disponible = False

        self.voces_emociones = {
            "neutral": "lumy_voces/Lumy-neutral.mp3",
            "curiosa": "lumy_voces/Lumy-curiosa.mp3",
            "entusiasmo": "lumy_voces/Lumy-entusiasmo.mp3",
            "confusion": "lumy_voces/Lumy-confusion.mp3",
            "empatia": "lumy_voces/Lumy-empatia.mp3",
            "frustracion": "lumy_voces/Lumy-frustracion.mp3",
            "preocupada": "lumy_voces/lumy-preocupada.mp3",
            "sorpresa": "lumy_voces/Lumy-sorpresa.mp3",
        }

        if TTS is not None:
            try:
                print("[LUMY VOZ] Cargando XTTS v2...")
                self.tts = TTS(
                    model_name="tts_models/multilingual/multi-dataset/xtts_v2"
                )
            except Exception as error:
                print("[LUMY VOZ] No se pudo cargar XTTS:", error)

        if pygame is not None:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                self.audio_disponible = True
            except Exception as error:
                print("[LUMY VOZ] No se pudo iniciar el audio:", error)

    def escuchar(self):
        try:
            with sr.Microphone() as fuente:
                print("[LUMY VOZ] Escuchando...")
                self.reconocedor.adjust_for_ambient_noise(
                    fuente, duration=0.5
                )
                audio = self.reconocedor.listen(fuente)

            texto = self.reconocedor.recognize_google(
                audio, language="es-BO"
            )
            print("[LUMY VOZ] Usuario:", texto)
            return texto

        except sr.UnknownValueError:
            print("[LUMY VOZ] No pude entender el mensaje.")
            return None
        except sr.RequestError as error:
            print("[LUMY VOZ] Error de reconocimiento:", error)
            return None
        except Exception as error:
            print("[LUMY VOZ] Error al escuchar:", error)
            return None

    def hablar(self, texto, emocion="neutral"):
        if not texto:
            return False

        if self.tts is None or not self.audio_disponible:
            print(
                "[LUMY VOZ] XTTS o el audio no están disponibles. "
                "El texto es:",
                texto,
            )
            return False

        emocion_key = emocion.lower()
        speaker_wav = self.voces_emociones.get(
            emocion_key,
            self.voces_emociones["neutral"],
        )

        if not os.path.isfile(speaker_wav):
            speaker_wav = self.voces_emociones["neutral"]

        if not os.path.isfile(speaker_wav):
            print("[LUMY VOZ] No se encontró audio de referencia.")
            return False

        output_filename = f"temp_lumy_{uuid.uuid4().hex}.wav"

        try:
            self.tts.tts_to_file(
                text=texto,
                speaker_wav=speaker_wav,
                language="es",
                file_path=output_filename,
            )

            pygame.mixer.music.load(output_filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            return True

        except Exception as error:
            print("[LUMY VOZ] Error al generar o reproducir voz:", error)
            return False

        finally:
            if pygame is not None and pygame.mixer.get_init():
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                except Exception:
                    pass

            try:
                if os.path.exists(output_filename):
                    os.remove(output_filename)
            except OSError:
                pass

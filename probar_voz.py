from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os

# Si notas que va muy lento o consume mucha memoria, puedes descomentar la siguiente línea:
# os.environ["SUNO_USE_SMALL_MODELS"] = "True"

print("Cargando los modelos de Bark (la primera vez descargará los pesos, ten paciencia)...")
preload_models()

# Elige un preset de voz en español (puedes probar del 0 al 9)
voice_preset = "v2/es_speaker_6"

# Texto de prueba con expresiones emocionales
text_prompt = "¡Hola! No puedo creer que hayamos llegado hasta aquí... [risas] ¡Esto es increíble!"

print("Generando el audio de tu personaje...")
audio_array = generate_audio(text_prompt, history_prompt=voice_preset)

# Guarda el resultado en un archivo de audio local
write_wav("voz_personaje.wav", SAMPLE_RATE, audio_array)
print("¡Listo! Audio guardado como 'voz_personaje.wav'. ¡Escúchalo para ver qué tal suena!")
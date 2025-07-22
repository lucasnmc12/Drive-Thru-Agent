
from kokoro import KPipeline
import soundfile as sf
import numpy as np

lang_code = "p"

pipeline = KPipeline(lang_code=lang_code)

text = """
Bem-vindo ao nosso drive-thru! Em que posso ajudar?
"""

generator = pipeline(text, voice='pm_santa')

audio_chunks = []

for gs, ps, audio in generator:
    audio_chunks.append(audio)

audio_completo = np.concatenate(audio_chunks)
sf.write('audio_completo.wav', audio_completo, 24000)



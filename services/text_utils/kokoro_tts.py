import pyaudio
import numpy as np
from kokoro import KPipeline

pipeline = KPipeline(repo_id='hexgrad/Kokoro-82M', lang_code='p')  # 'p' = português
pyaudio_instance = pyaudio.PyAudio()

def falar_com_kokoro(texto, voz='pf_dora'):
    stream = pyaudio_instance.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=24000,
        output=True
    )

    generator = pipeline(texto, voice=voz)

    audio_chunks = []
    for _, _, audio in generator:
        audio_chunks.append(audio)

    if audio_chunks:
        audio_completo = np.concatenate(audio_chunks)
        stream.write(audio_completo.tobytes())

    stream.stop_stream()
    stream.close()

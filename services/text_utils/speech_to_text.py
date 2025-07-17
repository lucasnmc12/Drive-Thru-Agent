import speech_recognition as sr

def transcrever(audio):
    recognizer = sr.Recognizer()

     # 🔧 Ajuste de tempo de pausa (padrão é 0.8 segundos)
    recognizer.pause_threshold = 1.5  # espere 1.5 segundos de silêncio antes de parar

    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        return texto
    except sr.UnknownValueError:
        return None
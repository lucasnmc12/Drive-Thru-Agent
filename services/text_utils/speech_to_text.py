import speech_recognition as sr

def transcrever(audio):
    recognizer = sr.Recognizer()

    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        return texto
    except sr.UnknownValueError:
        return None
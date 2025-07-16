import speech_recognition as sr


def ouvir_microfone():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Ouvindo...")
        audio = recognizer.listen(source)
    return audio
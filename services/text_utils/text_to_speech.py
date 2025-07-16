import pyttsx3
from services.text_utils.sanitize_text import limpar_texto_para_fala

def falar(texto):
    texto_limpo = limpar_texto_para_fala(texto)

    engine = pyttsx3.init()
    engine.setProperty('rate', 250) # acelera a fala, padrão = 200
    engine.say(texto_limpo)
    engine.runAndWait()


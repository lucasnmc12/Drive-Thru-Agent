import re

def limpar_texto_para_fala(texto):
    # Remove emojis
    texto = re.sub(r"[^\w\s,.!?]", "", texto)

    # Remove palavras tipo "emoji de", "símbolo de", etc.
    texto = re.sub(r"emoji de \w+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"símbolo de \w+", "", texto, flags=re.IGNORECASE)

    # Remove repetições de pontuação desnecessária
    texto = re.sub(r"([,.!?])\1+", r"\1", texto)

    # Remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto
import re

def limpar_texto_para_fala(texto):
    # Remove emojis
    texto = re.sub(r"[^\w\s,.!?]", "", texto)

    # Remove palavras tipo "emoji de", "símbolo de", etc.
    texto = re.sub(r"emoji de \w+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"símbolo de \w+", "", texto, flags=re.IGNORECASE)

    texto = re.sub(r"(R\$|R)?\s?(\d+)[,.](\d{2})", lambda m: f"{m.group(2)} reais e {m.group(3)}", texto)

    # Converte "Mc" ou "mc" para "mec"
    texto = re.sub(r"\b[Mm]c", "mec", texto)
    texto = re.sub(r"\b[Mm]ac", "mec", texto)

    # Remove repetições de pontuação desnecessária
    texto = re.sub(r"([,.!?])\1+", r"\1", texto)

    # Remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto
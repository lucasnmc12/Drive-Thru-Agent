import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_LUCAS")

genai.configure(api_key=GEMINI_API_KEY)

# ✳️ Inicia o modelo com histórico
modelo = genai.GenerativeModel("gemini-2.5-flash")
conversa = modelo.start_chat(history = [
    {"role": "user", "parts": ["Oi"]},
    {"role": "model", "parts": ["Olá! Seja bem-vindo ao nosso drive-thru. O que deseja pedir hoje?"]}
])

def obter_resposta(texto_cliente):
    resposta = conversa.send_message(f"""A seguinte frase foi dita pelo cliente:
                                     
    "{texto_cliente}"

        1. Continue a conversa normalmente, como atendente de drive-thru.
        2. Ao final da sua resposta, diga: [ENCERRAR=sim] se o cliente deu a entender que deseja encerrar o pedido, ou [ENCERRAR=nao] se não deu.
        Responda de forma educada como sempre.
        """)
    
    conteudo = resposta.text
    resposta_limpa = conteudo.replace("[ENCERRAR=sim]", "").replace("[ENCERRAR=nao]", "").strip()
    encerrar = "ENCERRAR=sim" in conteudo


    return resposta_limpa, encerrar
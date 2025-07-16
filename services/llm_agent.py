import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests


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

    # busca semantica nos produtos
    try:
        resposta_busca = requests.post(
            "http://localhost:8000/search",
            json={"query": texto_cliente, "limite": 3}
        )
        produtos = resposta_busca.json()
        print("🧪 produtos:", produtos)
        print("📦 tipo:", type(produtos))
    except Exception as e:
        produtos = []
        print("Erro na busca semantica:", e)


    # 🧾 Monta contexto de produtos encontrados
    if produtos:
        produtos_texto = "\n".join([
            f"- {p['nome']}: {p['descricao']} (R${p['preco']})" for p in produtos
        ])
        contexto_produtos = f"\nEsses são os produtos mais relevantes para o pedido:\n{produtos_texto}\n"
    else:
        contexto_produtos = "\n(Nenhum produto relevante foi encontrado.)"

        # ✨ Prompt para o modelo
    prompt = f"""A seguinte frase foi dita pelo cliente:

        "{texto_cliente}"

        {contexto_produtos}

        1. Use os produtos listados acima como base para entender e responder.
        2. Continue a conversa como um atendente de drive-thru.
        3. Ao final da resposta, diga: [ENCERRAR=sim] se o cliente quiser encerrar o pedido, ou [ENCERRAR=nao] caso contrário.
        Responda de forma simpática e clara.
        """

        
    resposta = conversa.send_message(prompt)
    
    conteudo = resposta.text
    resposta_limpa = conteudo.replace("[ENCERRAR=sim]", "").replace("[ENCERRAR=nao]", "").strip()
    encerrar = "ENCERRAR=sim" in conteudo


    return resposta_limpa, encerrar
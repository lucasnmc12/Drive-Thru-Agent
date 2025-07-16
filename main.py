from services.microphone import ouvir_microfone
from services.text_utils.speech_to_text import transcrever
from services.llm_agent import obter_resposta
from services.text_utils.text_to_speech import falar


print("🤖 Atendente IA iniciado. Diga 'encerrar pedido' para sair.")

confirmando_encerramento = False

while True:
    audio = ouvir_microfone()
    texto = transcrever(audio)

    if not texto:
        falar("Não entendi. Pode repetir, por favor?")
        continue

    print(f"🧍 Cliente: {texto}")

    if confirmando_encerramento:
        if "sim" in texto.lower():
             falar("Pedido encerrado. Obrigado e volte sempre!")
             break
        else:
             falar("Pedido ainda em andamento. Pode continuar")
             confirmando_encerramento = False
             continue
        
    resposta, quer_encerrar = obter_resposta(texto)
    print(""f"🤖 Agente: {resposta}""")
    falar(resposta)

    if quer_encerrar:
        confirmando_encerramento = True
        falar ("Você deseja realmente encerrar o pedido?")

    
from services.microphone import ouvir_microfone
from services.text_utils.speech_to_text import transcrever
from services.llm_agent import obter_resposta
from services.text_utils.text_to_speech import falar
from services.text_utils.sanitize_text import limpar_texto_para_fala
from services.text_utils.kokoro_tts import falar_com_kokoro
from services.text_utils.kokoro_tts import pyaudio_instance




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

    fala_formatada = limpar_texto_para_fala(resposta)
    falar_com_kokoro (fala_formatada)
    #print(f"Texto limpo:{fala_formatada}")

    if quer_encerrar:
        confirmando_encerramento = True
        falar ("Você deseja realmente encerrar o pedido?")

        pyaudio_instance.terminate()

    
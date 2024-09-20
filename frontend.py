import streamlit as st
from audio_recorder_streamlit import audio_recorder
import backend
from PIL import Image
import base64

#Base Functions
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

#Bot Functions
def open_convo_bot(client,thread_id, assistant_id):
    recorded_audio = audio_recorder()
    if recorded_audio:
        audio_file = 'audio.mp3'
        with open(audio_file, 'wb') as f:
            f.write(recorded_audio)
        
        transcribed_text = backend.audio_to_text(audio_file,client)
        st.write(f"Texto transcrito: {transcribed_text}")
        
        response_text = backend.op_get_assistant_response(transcribed_text,client,thread_id,assistant_id)
        st.write(f"Resposta do chatbot: {response_text}")
        
        response_audio = 'response_audio.mp3'
        backend.text_to_audio(response_text, response_audio,client)
        st.audio(response_audio)

def img_convo_bot(client,key):
    if 'vbase64_image' not in st.session_state:
        st.session_state.vbase64_image = None
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'img_path' not in st.session_state:
        st.session_state.img_path = None

    if st.session_state.vbase64_image is None:
        st.session_state.uploaded_file = st.file_uploader("Escolha uma imagem para guiar a conversa!", type=["jpg"])

        if st.session_state.uploaded_file:
            image = Image.open(st.session_state.uploaded_file)
            st.session_state.img_path = "image.jpg"
            image.save(st.session_state.img_path)
            st.session_state.vbase64_image = encode_image(st.session_state.img_path)
            st.image(st.session_state.img_path, caption="Imagem Selecionada para Conversa", width=200)
            st.success("Imagem carregada com sucesso! Agora você pode gravar o áudio.")
    
    if st.session_state.vbase64_image is not None:
        recorded_audio = audio_recorder()

        if recorded_audio:
            audio_file = 'audio.mp3'
            with open(audio_file, 'wb') as f:
                f.write(recorded_audio)

            transcribed_text = backend.audio_to_text(audio_file, client)
            st.write(f"Texto transcrito: {transcribed_text}")

            response_text = backend.img_get_assistant_response(transcribed_text, st.session_state.vbase64_image, key)
            st.write(f"Resposta do chatbot: {response_text}")

            response_audio = 'response_audio.mp3'
            backend.text_to_audio(response_text, response_audio, client)
            st.audio(response_audio)

def pdf_convo_bot(client,thread_id,assistant_id):
    if 'set_pdf' not in st.session_state:
        st.session_state.set_pdf = None
    if 'uploaded_pdf' not in st.session_state:
        st.session_state.uploaded_pdf = None
    if 'file_id' not in st.session_state:
        st.session_state.file_id = None

    if st.session_state.set_pdf is None:
        st.session_state.uploaded_pdf = st.file_uploader("Escolha um PDF para guiar a conversa!", type=["pdf"])
        if st.session_state.uploaded_pdf:
            with open("pdf.pdf", "wb") as f:
                f.write(st.session_state.uploaded_pdf.getbuffer())
                st.success("Pdf carregado com sucesso! Agora você pode gravar o áudio.")
            
            message_file = client.files.create(
                file=open("pdf.pdf", "rb"), purpose="assistants"
            )
            st.session_state.file_id = message_file.id
            st.session_state.set_pdf = True

    if st.session_state.set_pdf is not None and st.session_state.file_id is not None:
        recorded_audio = audio_recorder()
        if recorded_audio:
            audio_file = 'audio.mp3'
            with open(audio_file, 'wb') as f:
                f.write(recorded_audio)
            
            transcribed_text = backend.audio_to_text(audio_file, client)
            st.write(f"Texto transcrito: {transcribed_text}")
            
            response_text = backend.pdf_get_assistant_response(st.session_state.file_id, transcribed_text, client, thread_id, assistant_id)
            st.write(f"Resposta do chatbot: {response_text}")
            
            response_audio = 'response_audio.mp3'
            backend.text_to_audio(response_text, response_audio, client)
            st.audio(response_audio)

#Main App
def main():
    if 'bot_selecionado' not in st.session_state:
        st.session_state.bot_selecionado = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'client' not in st.session_state:
        st.session_state.client = None

    if st.session_state.bot_selecionado is None:
        st.session_state.api_key = st.text_input("Digite sua chave da API da OpenAI", type="password")
        if st.session_state.api_key:
            st.session_state.client = backend.set_key(st.session_state.api_key)
            st.success("API Key validada e assistente configurado. Você pode começar a gravar áudios.")

            opcao = st.radio(
                "Selecione um Bot:",
                ('Conversa Aberta', 'Conversa de Imagem', 'Conversa de PDF')
            )
            if opcao == 'Conversa Aberta':
                thread_id, assistant_id = backend.op_set_assistant(st.session_state.client)
                st.session_state.bot_selecionado = open_convo_bot(st.session_state.client,thread_id, assistant_id)
            elif opcao == 'Conversa de Imagem':
                st.session_state.bot_selecionado = img_convo_bot(st.session_state.client, st.session_state.api_key)
            elif opcao == 'Conversa de PDF':
                thread_id, assistant_id = backend.pdf_set_assistant(st.session_state.client)
                st.session_state.bot_selecionado = pdf_convo_bot(st.session_state.client,thread_id, assistant_id)

    else:
        if st.session_state.bot_selecionado == "Conversa Aberta":
            open_convo_bot(st.session_state.client,thread_id, assistant_id)
        elif st.session_state.bot_selecionado == "Conversa de Imagem":
            img_convo_bot(st.session_state.client,st.session_state.api_key)
        elif st.session_state.bot_selecionado == "Conversa de PDF":
            pdf_convo_bot(st.session_state.client,thread_id, assistant_id)

        if st.button("Trocar de Bot"):
            st.session_state.bot_selecionado = None

st.title("Language Practice Chatbot")

if __name__ == '__main__':
    main()

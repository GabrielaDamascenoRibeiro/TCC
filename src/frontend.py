import streamlit as st
from audio_recorder_streamlit import audio_recorder
import backend as backend
from PIL import Image
import base64

#Base Functions
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def user_input_form():
    with st.form("form"):
        name = st.text_input("Name")
        pronouns = st.text_input("Pronouns")
        study_language = st.text_input("Study Language")
        level = st.selectbox("Level of Knowledge", ["Beginner", "Intermediate", "Advanced"])
        
        submitted = st.form_submit_button("Start")
        
        if submitted:
            st.session_state["user_info"] = {
                "name": name,
                "pronouns": pronouns,
                "study_language": study_language,
                "level": level
            }
            st.success("Information saved!")

#Bot Functions
def open_convo_bot(user_info, client,thread_id, assistant_id):
    recorded_audio = audio_recorder()
    if recorded_audio:
        audio_file = 'data\\audio.mp3'
        with open(audio_file, 'wb') as f:
            f.write(recorded_audio)
        
        transcribed_text = backend.audio_to_text(audio_file,client)
        st.write(f"USER: {transcribed_text}")
        
        response_text = backend.op_get_assistant_response(user_info, transcribed_text,client,thread_id,assistant_id)
        st.write(f"CHATBOT: {response_text}")
        
        response_audio = 'data\\response_audio.mp3'
        backend.text_to_audio(response_text, response_audio,client)
        st.audio(response_audio)

def img_convo_bot(user_info,client,key):
    if 'vbase64_image' not in st.session_state:
        st.session_state.vbase64_image = None
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'img_path' not in st.session_state:
        st.session_state.img_path = None

    if st.session_state.vbase64_image is None:
        st.session_state.uploaded_file = st.file_uploader("Load an image (jpg) to start the conversation!", type=["jpg"])

        if st.session_state.uploaded_file:
            image = Image.open(st.session_state.uploaded_file)
            st.session_state.img_path = "data\\image.jpg"
            image.save(st.session_state.img_path)
            st.session_state.vbase64_image = encode_image(st.session_state.img_path)
            st.image(st.session_state.img_path, caption="Imagem Selected", width=200)
            st.success("Image loaded successfully!")
    
    if st.session_state.vbase64_image is not None:
        recorded_audio = audio_recorder()

        if recorded_audio:
            audio_file = 'data\\audio.mp3'
            with open(audio_file, 'wb') as f:
                f.write(recorded_audio)

            transcribed_text = backend.audio_to_text(audio_file, client)
            st.write(f"USER: {transcribed_text}")

            response_text = backend.img_get_assistant_response(user_info, transcribed_text, st.session_state.vbase64_image, key)
            st.write(f"CHATBOT: {response_text}")

            response_audio = 'data\\response_audio.mp3'
            backend.text_to_audio(response_text, response_audio, client)
            st.audio(response_audio)

def pdf_convo_bot(user_info, client,thread_id,assistant_id):
    if 'set_pdf' not in st.session_state:
        st.session_state.set_pdf = None
    if 'uploaded_pdf' not in st.session_state:
        st.session_state.uploaded_pdf = None
    if 'file_id' not in st.session_state:
        st.session_state.file_id = None

    if st.session_state.set_pdf is None:
        st.session_state.uploaded_pdf = st.file_uploader("Load a PDF to start the conversation!", type=["pdf"])
        if st.session_state.uploaded_pdf:
            with open("data\\pdf.pdf", "wb") as f:
                f.write(st.session_state.uploaded_pdf.getbuffer())
                st.success("Pdf loaded successfully!")
            
            message_file = client.files.create(
                file=open("data\\pdf.pdf", "rb"), purpose="assistants"
            )
            st.session_state.file_id = message_file.id
            st.session_state.set_pdf = True

    if st.session_state.set_pdf is not None and st.session_state.file_id is not None:
        recorded_audio = audio_recorder()
        if recorded_audio:
            audio_file = 'data\\audio.mp3'
            with open(audio_file, 'wb') as f:
                f.write(recorded_audio)
            
            transcribed_text = backend.audio_to_text(audio_file, client)
            st.write(f"USER: {transcribed_text}")
            
            response_text = backend.pdf_get_assistant_response(user_info, st.session_state.file_id, transcribed_text, client, thread_id, assistant_id)
            st.write(f"CHATBOT: {response_text}")
            
            response_audio = 'data\\response_audio.mp3'
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
        st.session_state.api_key = st.text_input("Type your OpenAI API Key", type="password")
        if st.session_state.api_key:
            st.session_state.client = backend.set_key(st.session_state.api_key)
            st.success("API Key validated!")
            if 'user_info' not in st.session_state:
                user_input_form()
            else:
                user_info = st.session_state["user_info"]
                st.write(f"Welcome, {user_info['name']}!")
                st.write(f"Pronouns: {user_info['pronouns']}")
                st.write(f"Study Language: {user_info['study_language']} ({user_info['level']})")
                
                opcao = st.radio(
                    "Select a bot:",
                    ('Open Conversation', 'Image Based Conversation', 'PDF Based Conversation')
                )
                if opcao == 'Open Conversation':
                    thread_id, assistant_id = backend.op_set_assistant(user_info, st.session_state.client)
                    st.session_state.bot_selecionado = open_convo_bot(user_info['study_language'], st.session_state.client,thread_id, assistant_id)
                elif opcao == 'Image Based Conversation':
                    st.session_state.bot_selecionado = img_convo_bot(user_info, st.session_state.client, st.session_state.api_key)
                elif opcao == 'PDF Based Conversation':
                    thread_id, assistant_id = backend.pdf_set_assistant(user_info, st.session_state.client)
                    st.session_state.bot_selecionado = pdf_convo_bot(user_info['study_language'], st.session_state.client,thread_id, assistant_id)

    else:
        if st.session_state.bot_selecionado == "Open Conversation":
            open_convo_bot(user_info['study_language'], st.session_state.client,thread_id, assistant_id)
        elif st.session_state.bot_selecionado == "Image Based Conversation":
            img_convo_bot(user_info, st.session_state.client,st.session_state.api_key)
        elif st.session_state.bot_selecionado == "PDF Based Conversation":
            pdf_convo_bot(user_info['study_language'],st.session_state.client,thread_id, assistant_id)

        if st.button("Change Bot"):
            st.session_state.bot_selecionado = None

st.title("Language Practice Chatbot")

if __name__ == '__main__':
    main()

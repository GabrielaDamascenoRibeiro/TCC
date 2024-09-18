import streamlit as st
from audio_recorder_streamlit import audio_recorder
import backend

def bot_start():
    recorded_audio = audio_recorder()
    if recorded_audio:
        audio_file = 'audio.mp3'
        with open(audio_file, 'wb') as f:
            f.write(recorded_audio)
        
        transcribed_text = backend.transcribe_audio_with_whisper(audio_file, st.session_state.client)
        st.write(f"Texto transcrito: {transcribed_text}")
        
        response_text = backend.get_assistant_response(transcribed_text, st.session_state.client, st.session_state.thread_id, st.session_state.assistant_id)
        st.write(f"Resposta do chatbot: {response_text}")
        
        response_audio = 'response_audio.mp3'
        backend.text_to_audio(response_text, response_audio, st.session_state.client)
        st.audio(response_audio)

st.title("English Practice Chatbot")

if 'client' not in st.session_state:
    api_key = st.text_input("Digite sua chave da API da OpenAI", type="password")

    if api_key:
        st.session_state.client = backend.set_key(api_key)
        st.session_state.thread_id, st.session_state.assistant_id = backend.set_assistant(st.session_state.client)
        st.success("API Key validada e assistente configurado. Você pode começar a gravar áudios.")
        bot_start()
else:
    bot_start()
    
#key: sk-hTkXQgSv6FHdbQiN318PdNy9QZQfp-_n6-GZc0FoFiT3BlbkFJuyh1urSnrm3CVQzUrSrkSVL4LNCxec1LMR99LzvCUA
# frontend.py
import streamlit as st
import requests

backend_url = "http://localhost:8000/analyze"

st.title("Visual Personal Assistant")

context = []

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    user_input = st.text_input("Ask a question about the image:")

    if st.button("Submit"):
        files = {"file": uploaded_file.getvalue()}
        data = {"context": "|||".join(context), "user_input": user_input}
        response = requests.post(backend_url, files=files, data=data)
        bot_response = response.json().get("response", "")

        st.write("Assistant:", bot_response)
        context.append(f"User: {user_input}")
        context.append(f"Assistant: {bot_response}")

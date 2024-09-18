# English Practice Chatbot

This project is an English practice chatbot that allows users to converse with an AI and practice their speaking skills. The system accepts audio inputs, transcribes them using OpenAI's Whisper API, interacts with the OpenAI API, and provides audio responses.

## Features

- Record audio files for conversation.
- Receive transcriptions of your audio.
- Get responses from the chatbot.
- Listen to audio responses from the chatbot.

## Requirements

- Python 3.7+
- OpenAI API Key

## Estrutura do projeto

seu-repositorio/
├── backend.py
├── frontend.py
├── requirements.txt
└── README.md

## Configuração

### Passo 1: Clonar o repositório

git clone 
cd 

### Passo 2: Criar um ambiente virtual (opcional, mas recomendado)

python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

### Passo 3: Instalar as dependências

pip install -r requirements.txt

### Passo 5: Executar a aplicação

streamlit run frontend.py

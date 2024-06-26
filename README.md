# Visual Personal Assistant

Este projeto utiliza transformadores de visão e a API OpenAI para criar um assistente pessoal visual que pode analisar imagens e responder perguntas sobre elas.

## Estrutura do projeto

seu-repositorio/
├── backend.py
├── frontend.py
├── requirements.txt
└── README.md

## Configuração

### Passo 1: Clonar o repositório

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

### Passo 2: Criar um ambiente virtual (opcional, mas recomendado)

python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

### Passo 3: Instalar as dependências

pip install -r requirements.txt

### Passo 4: Configurar a chave da API OpenAI

Substitua 'YOUR_OPENAI_API_KEY' no arquivo backend.py pela sua chave de API da OpenAI.

### Passo 5: Executar a aplicação

streamlit run frontend.py
Open your web browser and go to http://localhost:8501.

## Usage

1. Upload an image.
2. Ask a question about the image.
3. The assistant will analyze the image and respond to your question.
4. Continue the conversation by asking follow-up questions.

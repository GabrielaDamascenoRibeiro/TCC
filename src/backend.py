from openai import OpenAI
import requests

#Base Functions
def set_key(api_key):
    return (OpenAI(api_key = api_key))

def text_to_audio(text, audio, client):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
    )
    response.stream_to_file(audio)

def audio_to_text(audio_file, client): 
    with open (audio_file, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return response.text

#Open Convo Assistants
def op_set_assistant(client):
    assistant = client.beta.assistants.create(
        name="English Teacher",
        instructions="You are a personal english conversational teacher, your goal is to keep an english conversation going and correcting eventual mistakes. Do your best to always keep a conversation, and only speak in the student's native language if necessary.",
        model="gpt-4o"
    )
    thread = client.beta.threads.create()
    thread_id = thread.id
    assistant_id = assistant.id
    return (thread_id, assistant_id)

def op_get_assistant_response(text,client,thread_id, assistant_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions= "Please address the user as Gabi. Gabi is a Portuguese native speaker who needs to practice her english conversation skills."
    )
    
    import time
    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    return messages.data[0].content[0].text.value

#Img Convo Assistants
def img_get_assistant_response(text, img, client):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {client}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", 
         "content": "You are a personal english conversational teacher, your goal is to keep an english conversation going and correcting eventual mistakes. Do your best to always keep a conversation, and only speak in the student's native language if necessary. Please address the user as Gabi. Gabi is a Portuguese native speaker who needs to practice her english conversation skills."
        },
        {
        "role": "user",
        "content": [
                {
                "type": "text",
                "text": text
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img}"
                }
                }
            ]
        }
    ],
    "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    response_data = response.json()
    return response_data['choices'][0]['message']['content']


#Pdf Convo Assistants
def pdf_set_assistant(client):
    assistant = client.beta.assistants.create(
        name="English Teacher",
        instructions="You are a personal english conversational teacher, your goal is to keep an english conversation going and correcting eventual mistakes. Do your best to always keep a conversation, and only speak in the student's native language if necessary.",
        model="gpt-4o",
        tools=[{"type": "file_search"}]
    )
    thread = client.beta.threads.create()
    thread_id = thread.id
    assistant_id = assistant.id
    return (thread_id, assistant_id)

def pdf_get_assistant_response(file, text,client,thread_id, assistant_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text,
        attachments=[{"file_id": file, "tools": [{"type": "file_search"}]}]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions= "Please address the user as Gabi. Gabi is a Portuguese native speaker who needs to practice her english conversation skills. Use the attached file as context for the conversation."
    )
    
    import time
    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    return messages.data[0].content[0].text.value
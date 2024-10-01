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
def op_set_assistant(user_info, client):
    assistant = client.beta.assistants.create(
        name="Personal Conversational Teacher",
        instructions=f"You are a personal conversational teacher, your goal is to keep a conversation going and correcting eventual language mistakes. About your student, Name:{user_info['name']}, Pronouns: {user_info['pronouns']}, Studying the language:{user_info['study_language']} at level {user_info['level']}. ONLY RESPOND AND SPEAK in the language the student is trying to practice and learn. DO NOT speak in any language apart from the studying language.",
        model="gpt-4o"
    )
    thread = client.beta.threads.create()
    thread_id = thread.id
    assistant_id = assistant.id
    return (thread_id, assistant_id)

def op_get_assistant_response(user_info,text,client,thread_id,assistant_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions= f"ONLY SPEAK AND RESPOND IN {user_info} LANGUAGE. Keep a conversation. Correct eventual language mistakes. Try to teach something new in the language the student is trying to practice and learn."
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
def img_get_assistant_response(user_info, text, img, client):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {client}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", 
         "content": f"Use the image as context for the conversation. You are a personal conversational teacher, your goal is to keep a conversation going and correcting eventual language mistakes. About your student, Name:{user_info['name']}, Pronouns: {user_info['pronouns']}, Studying the language:{user_info['study_language']} at level {user_info['level']}. ONLY RESPOND AND SPEAK in the language the student is trying to practice and learn. DO NOT speak in any language apart from the studying language. Try to teach something new in the language the student is trying to practice and learn."
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
def pdf_set_assistant(user_info, client):
    assistant = client.beta.assistants.create(
        name="English Teacher",
        instructions=f"You are a personal conversational teacher, your goal is to keep a conversation going and correcting eventual language mistakes. About your student, Name:{user_info['name']}, Pronouns: {user_info['pronouns']}, Studying the language:{user_info['study_language']} at level {user_info['level']}. ONLY RESPOND AND SPEAK in the language the student is trying to practice and learn. DO NOT speak in any language apart from the studying language.",
        model="gpt-4o",
        tools=[{"type": "file_search"}]
    )
    thread = client.beta.threads.create()
    thread_id = thread.id
    assistant_id = assistant.id
    return (thread_id, assistant_id)

def pdf_get_assistant_response(user_info, file, text,client,thread_id, assistant_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text,
        attachments=[{"file_id": file, "tools": [{"type": "file_search"}]}]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions= f"Use the attached file as context for the conversation. ONLY SPEAK AND RESPOND IN {user_info} LANGUAGE. Keep a conversation. Correct eventual language mistakes. Try to teach something new in the language the student is trying to practice and learn."
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
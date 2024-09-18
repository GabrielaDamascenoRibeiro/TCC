from openai import OpenAI

def set_key(api_key):
    return (OpenAI(api_key = api_key))

def set_assistant(client):
    assistant = client.beta.assistants.create(
        name="English Teacher",
        instructions="You are a personal english conversational teacher, your goal is to keep an english conversation going and correcting eventual mistakes. Do your best to always keep a conversation, and only speak in the student's native language if necessary.",
        model="gpt-4o"
    )
    thread = client.beta.threads.create()
    thread_id = thread.id
    assistant_id = assistant.id
    return (thread_id, assistant_id)

def transcribe_audio_with_whisper(audio_file, client): 
    with open (audio_file, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return response.text

def get_assistant_response(text,client,thread_id, assistant_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=text
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as Gabi. Gabi is a Portuguese native speaker who needs to practice her english conversation skills."
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

def text_to_audio(text, audio, client):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(audio)
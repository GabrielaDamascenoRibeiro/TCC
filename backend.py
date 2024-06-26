# backend.py
import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import openai
import io
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Load ViT model and feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

# Set OpenAI API key
openai.api_key = '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'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    return model.config.id2label[predicted_class_idx]

def generate_response(prompt, context=[]):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages += [{"role": "user", "content": msg} for msg in context]
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message['content']

class Context(BaseModel):
    context: list
    user_input: str

@app.post("/analyze")
async def process_image_and_respond(file: UploadFile, context: str = Form(...), user_input: str = Form(...)):
    image_bytes = await file.read()
    context = context.split("|||")
    image_analysis = analyze_image(image_bytes)
    full_prompt = f"Image analysis: {image_analysis}. User question: {user_input}"
    response = generate_response(full_prompt, context)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

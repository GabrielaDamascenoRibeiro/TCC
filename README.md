# Application of Generative AI in Language Practice: Creating a Multimodal Conversational Chatbot with OpenAI API

## Project Description
This project is part of the undergraduate thesis that explores the application of generative AI in language learning. The main objective is to develop a multimodal conversational chatbot using the OpenAI API, capable of interacting with users intuitively and effectively to facilitate language practice.

## Technologies Used
- OpenAI API: For generating intelligent responses and processing multimodal data.
- Streamlit: Framework used to build the web application frontend.
- Python: Primary programming language.

## Features
- Multimodal support: The chatbot processes and responds to various input types, such as audio, text, and images (when available).
- Automatic translation: Integrated functionality for translating conversations between different languages.
- Real-time feedback: The chatbot provides instant feedback during language practice.

## Project Structure
This repository contains two main components:
1. src: That contains the source files:
  
  1.1. Backend (backend.py): Responsible for the chatbot’s logic, OpenAI API integration, and multimodal data processing (audio, text, image).
  
  1.2. Frontend (frontend.py): Built with Streamlit, it provides a user-friendly interface for interacting with the chatbot.

2. data: Contains the data files used in the chatbots:
  
  2.1. MP3 files to store the audio files used by the user input (audio.mp3) and by the chatbot output (response_audio.mp3).
  
  2.2. JPG file to store the image (image.jpg) file from the image based chatbot.
  
  2.3. PDF file to store the pdf (pdf.pdf) file used in the PDF based chatbot.

## Requirements
- OpenAI API Key

## How to Run the Project
### 1: Install requirements

pip install -r requirements.txt

### 2: run app logic

python backend.py

### 3: run frontend

streamlit run frontend.py

## Contact
For more information, contact:

Name: Gabriela Damasceno Ribeiro

Linkedin: [gabrieladamascenoribeiro](https://www.linkedin.com/in/gabrieladamascenoribeiro/)

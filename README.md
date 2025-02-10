# Voice Chat Bot

## Installation and Setup

Follow these steps to set up and run the voice chat bot:

### 1. Clone the Repository
```sh
git clone https://github.com/Vikas-ABD/voice_chat_bot.git
cd voice_chat_bot
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Run the Application
```sh
streamlit run app.py
```
This will start the Streamlit interface for the voice chat bot.

---

## Flow of the Application

### **1. Audio to Text Conversion**
- The user speaks, and their voice input is recorded.
- The recorded audio file is sent to Groq's API for transcription.
- **Model Used:** `distil-whisper-large-v3-en`
- **API Call:**
  ```python
  transcription = client.audio.transcriptions.create(
      file=(audio_file_path, file.read()),
      model="distil-whisper-large-v3-en",
      response_format="verbose_json",
  )
  ```
- The API returns a **detailed JSON response** containing the transcribed text.

### **2. Processing with LLM**
- The transcribed text is sent to Groq's LLM for generating a response.
- **Model Used:** `deepseek-r1-distill-llama-70b`
- **API Key** is required for authentication.
- The LLM processes the input and generates a meaningful response.

### **3. Text to Speech Conversion**
- The generated text response is converted into speech using **Kokoro 82M** (a locally running TTS model).
- **Pipeline:**
  ```python
  audio_file = text_to_speech(full_response)
  ```
- The generated speech is played back to the user.

### **4. Complete Voice Chat Bot Experience**
- The application integrates **speech-to-text, LLM processing, and text-to-speech** to create a full **voice-based chatbot**.
- Users can **speak to the bot, receive AI-generated responses, and hear the responses spoken back to them**.

---

## Requirements
- Python 3.8+
- Streamlit
- Groq API Key
- Kokoro TTS Model

Enjoy using your **Voice Chat Bot!** 🎙️🤖
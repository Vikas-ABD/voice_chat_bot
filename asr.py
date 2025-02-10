import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio using Groq's Whisper model.
    Args:
        audio_file_path: Path to the audio file (WAV/MP3/M4A)
    Returns:
        Transcribed text (str) or error message.
    """
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),  # Pass file as tuple (filename, file_content)
                model="distil-whisper-large-v3-en",  # Model for English transcription
                response_format="verbose_json",      # Get detailed JSON response
            )
            return transcription.text.strip()  # Extract transcribed text from JSON
    except Exception as e:
        print(f"Transcription error: {e}")
        return "Could not transcribe audio. Please try again."
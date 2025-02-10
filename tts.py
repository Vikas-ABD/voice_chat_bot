from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment  # Import pydub for volume control

# Initialize the Kokoro pipeline
pipeline = KPipeline(lang_code='a')  # 'a' for American English

def text_to_speech(text: str, voice: str = 'af_heart', speed: float = 1.0, volume_boost: float = 6.0) -> str:
    """
    Convert text to speech using Kokoro TTS and increase volume.

    Args:
        text (str): The text to convert to speech.
        voice (str): The voice to use (default is 'af_heart').
        speed (float): The speed of speech (default is 1.0).
        volume_boost (float): Increase volume in dB (default is 6.0dB).

    Returns:
        str: The file path of the generated audio file.
    """
    try:
        # Generate audio using Kokoro
        generator = pipeline(
            text, voice=voice, speed=speed, split_pattern=r'\n+'
        )

        # Combine all audio chunks into one
        combined_audio = []
        for _, _, audio in generator:
            combined_audio.extend(audio)

        # Save the combined audio to a file
        temp_file_path = f"tts_output_temp.wav"
        sf.write(temp_file_path, combined_audio, 24000)

        # Load the audio and boost volume
        sound = AudioSegment.from_wav(temp_file_path)
        louder_sound = sound + volume_boost  # Increase volume (default +6dB)

        # Save the louder audio
        final_file_path = f"tts_output_{voice}.wav"
        louder_sound.export(final_file_path, format="wav")

        return final_file_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

import streamlit as st
from llm import generate_streaming_response
from asr import transcribe_audio
from tts import text_to_speech
import soundfile as sf
import sounddevice as sd
import os
import numpy as np
from datetime import datetime
import base64

# App configuration
st.set_page_config(page_title="AI Voice Assistant", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🎙️ AI Voice Assistant</h1>
    <hr style='border: 1px solid #4CAF50;'>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None
if "show_conversation" not in st.session_state:
    st.session_state.show_conversation = False

# Custom CSS for better UI
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    .user-message {
        background-color: #2b313e;
        color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 2px 2px 10px rgba(0, 255, 0, 0.3);
    }
    .bot-message {
        background-color: #1f252e;
        color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 2px 2px 10px rgba(0, 255, 255, 0.3);
    }
    .stAudio audio {
        width: 100% !important;
    }
    .conversation-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 10px;
        background-color: #0e1117;
        border-radius: 12px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

def record_audio():
    duration = st.slider("🎙️ Set recording duration (seconds)", 1, 10, 5)
    if st.button("🔴 Start Recording"):
        with st.spinner(f"Recording for {duration} seconds..."):
            fs = 16000
            audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            st.session_state.audio_data = (fs, audio_data)
            st.success("✅ Recording complete!")

def save_audio():
    if st.session_state.audio_data:
        fs, data = st.session_state.audio_data
        file_path = f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
        sf.write(file_path, data, fs, format="WAV")
        return file_path
    return None

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎤 Voice Input")
    record_audio()
    
    if st.session_state.audio_data:
        audio_file = save_audio()
        if audio_file:
            with st.spinner("📝 Transcribing audio..."):
                user_input = transcribe_audio(audio_file)
                os.remove(audio_file)
            
            if user_input:
                st.session_state.conversation.append(("user", user_input))
                
                with st.spinner("🤖 Generating response..."):
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in generate_streaming_response(user_input):
                        full_response += chunk
                        response_placeholder.markdown(
                            f'<div class="bot-message">🤖 Assistant: {full_response}</div>', 
                            unsafe_allow_html=True
                        )
                    
                    st.session_state.conversation.append(("assistant", full_response))

            st.session_state.audio_data = None
                    
            if full_response:      
                with st.spinner("🔊 Generating voice response..."):
                    audio_file = text_to_speech(full_response)
                    if audio_file:
                        with open(audio_file, "rb") as f:
                            audio_bytes = f.read()
                            audio_base64 = base64.b64encode(audio_bytes).decode()

                        audio_html = f"""
                        <audio id="audioPlayer" autoplay>
                            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                        <script>
                            var audio = document.getElementById("audioPlayer");
                            audio.volume = 2;  // Increase volume (1.0 is default, 1.5 is louder)
                        </script>
                        """
                        st.markdown(audio_html, unsafe_allow_html=True)

                        os.remove(audio_file)

    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation = []
        st.rerun()

with col2:
    if st.button("📜 Show Conversation"):
        st.session_state.show_conversation = not st.session_state.show_conversation
    
    if st.session_state.show_conversation:
        st.subheader("Conversation History")
        conv_html = '<div class="conversation-container">'
        for role, message in st.session_state.conversation:
            if role == "user":
                conv_html += f'<div class="user-message">👤 User: {message}</div>'
            else:
                conv_html += f'<div class="bot-message">🤖 Assistant: {message}</div>'
        conv_html += '</div>'
        st.markdown(conv_html, unsafe_allow_html=True)
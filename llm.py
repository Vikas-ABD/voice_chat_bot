import os
from groq import Groq
from typing import Generator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_streaming_response(user_input: str) -> Generator[str, None, None]:
    """
    Generate concise streaming response using ONLY current input.
    Responses are limited to 3 lines or less.
    """
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise and helpful assistant. Always respond in 1 lines or less. Be direct and to the point. Avoid explanations unless explicitly asked."
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.4,
            max_tokens=100,  # Limit tokens to ensure short responses
            top_p=0.95,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print(f"Streaming Error: {e}")
        yield "I'm having trouble responding right now. Please try again."
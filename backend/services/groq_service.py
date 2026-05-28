import os
from groq import AsyncGroq
import tempfile

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    # Write to a temporary file since the Groq API requires a file object
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    try:
        with open(temp_path, "rb") as file:
            transcription = await client.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3",
                response_format="json",
            )
        return transcription.text
    finally:
        os.remove(temp_path)

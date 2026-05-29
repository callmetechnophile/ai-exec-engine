import os
from groq import AsyncGroq
import tempfile

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

async def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    # Extract extension or default to webm
    ext = os.path.splitext(filename)[1]
    if not ext:
        ext = ".webm"
        
    # Write to a temporary file since the Groq API requires a file object
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    try:
        with open(temp_path, "rb") as file:
            transcription = await client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3",
                response_format="text",
            )
        return transcription

    finally:
        os.remove(temp_path)

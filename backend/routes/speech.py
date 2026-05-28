from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import SpeechResponse
from services.groq_service import transcribe_audio

router = APIRouter()

@router.post("/speech-to-text", response_model=SpeechResponse)
async def speech_to_text(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = await transcribe_audio(content, file.filename)
        return SpeechResponse(text=text)
    except Exception as e:
        print(f"Error in speech-to-text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

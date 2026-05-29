from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.fal_service import generate_engineering_image

router = APIRouter()

class ImageGenerationRequest(BaseModel):
    query: str

class ImageGenerationResponse(BaseModel):
    base64_image: str

@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(req: ImageGenerationRequest):
    try:
        image_data = await generate_engineering_image(req.query)
        if not image_data:
            raise HTTPException(status_code=500, detail="Image generation failed or returned empty.")
        
        return ImageGenerationResponse(base64_image=image_data)
    except Exception as e:
        print(f"Error in generate-image route: {e}")
        raise HTTPException(status_code=500, detail=str(e))

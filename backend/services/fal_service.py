import os
import base64
from io import BytesIO
from huggingface_hub import AsyncInferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")

# Initialize the async client
client = AsyncInferenceClient(
    api_key=HF_TOKEN,
    timeout=120.0
)

async def generate_engineering_image(query: str) -> str:
    """
    Uses Hugging Face InferenceClient to generate a realistic engineering concept image.
    Returns a base64 encoded data URI to be rendered in the frontend.
    """
    if not HF_TOKEN:
        print("Warning: HF_TOKEN not set in keys.env")
        return ""
        
    MODELS = [
        "stabilityai/stable-diffusion-xl-base-1.0",
        "black-forest-labs/FLUX.1-schnell",
        "stabilityai/stable-diffusion-3.5-large",
        "stabilityai/stable-diffusion-2",
        "CompVis/stable-diffusion-v1-4",
        "runwayml/stable-diffusion-v1-5"
    ]
    
    prompt = f"A realistic, high-quality, modern engineering concept rendering of: {query}. Professional lighting, 3d CAD style."
    
    for model in MODELS:
        try:
            print(f"Attempting image generation with model: {model}")
            image = await client.text_to_image(
                prompt,
                model=model,
            )
            
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
            
    print("Error: All fallback image generation models failed on Hugging Face.")
    return ""

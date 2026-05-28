import os
import base64
from io import BytesIO
from huggingface_hub import AsyncInferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")

# Initialize the async client with the fal-ai provider
client = AsyncInferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN,
    timeout=120.0
)

async def generate_engineering_image(query: str) -> str:
    """
    Uses Hugging Face InferenceClient (routed to fal-ai) to generate a realistic engineering concept image.
    Returns a base64 encoded data URI to be rendered in the frontend.
    """
    if not HF_TOKEN:
        print("Warning: HF_TOKEN not set in keys.env")
        return ""
        
    try:
        prompt = f"A realistic, high-quality, modern engineering concept rendering of: {query}. Professional lighting, 3d CAD style."
        
        # text_to_image returns a PIL Image
        image = await client.text_to_image(
            prompt,
            model="Tongyi-MAI/Z-Image-Turbo",
        )
        
        # Convert the PIL Image to a Base64 data URI so Next.js can display it directly
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"Error generating image with HF/fal.ai: {e}")
        return ""

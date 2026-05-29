import os
import base64
import httpx
import urllib.parse
from io import BytesIO
from huggingface_hub import AsyncInferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")

async def generate_engineering_image(query: str) -> str:
    """
    Uses Pollinations.ai (Free, No API Key) as the primary generator.
    Falls back to Hugging Face InferenceClient if needed.
    """
    prompt = f"A realistic, high-quality, modern engineering concept rendering of: {query}. Professional lighting, 3d CAD style."
    
    # 1. Primary: Pollinations AI
    try:
        print("Attempting image generation with Pollinations.ai...")
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&width=1024&height=768"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            if response.status_code == 200:
                img_str = base64.b64encode(response.content).decode("utf-8")
                return f"data:image/jpeg;base64,{img_str}"
            else:
                print(f"Pollinations AI failed with status: {response.status_code}")
    except Exception as e:
        print(f"Pollinations AI exception: {e}")

    # 2. Secondary Fallbacks: Hugging Face Free Tier
    if HF_TOKEN:
        print("Falling back to Hugging Face...")
        client = AsyncInferenceClient(api_key=HF_TOKEN, timeout=120.0)
        MODELS = [
            "stabilityai/stable-diffusion-xl-base-1.0",
            "black-forest-labs/FLUX.1-schnell",
            "CompVis/stable-diffusion-v1-4"
        ]
        
        for model in MODELS:
            try:
                print(f"Attempting image generation with HF model: {model}")
                image = await client.text_to_image(prompt, model=model)
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                return f"data:image/png;base64,{img_str}"
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
                
    print("Error: All image generation engines failed.")
    return ""

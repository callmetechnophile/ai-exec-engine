import os
import base64
import httpx
import urllib.parse
import asyncio
from io import BytesIO
from huggingface_hub import AsyncInferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")

def get_fallback_svg(query: str) -> str:
    """
    Generates a futuristic technical blueprint SVG representation of the project
    to ensure the user always sees a beautiful mockup instead of a crash.
    """
    clean_query = query.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    short_query = clean_query[:45] + "..." if len(clean_query) > 45 else clean_query
    
    svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="100%" height="100%">
        <rect width="800" height="600" fill="#0b0f19"/>
        <defs>
            <pattern id="blueprint-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="1" opacity="0.6"/>
                <path d="M 200 0 L 0 0 0 200" fill="none" stroke="#334155" stroke-width="1.5" opacity="0.4"/>
            </pattern>
            <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.8"/>
            </linearGradient>
        </defs>
        <rect width="800" height="600" fill="url(#blueprint-grid)"/>
        
        <!-- Schematic Lines & Accents -->
        <circle cx="400" cy="300" r="160" fill="none" stroke="url(#glow)" stroke-width="1.5" stroke-dasharray="12 6" opacity="0.4"/>
        <circle cx="400" cy="300" r="120" fill="none" stroke="#6366f1" stroke-width="2" opacity="0.6"/>
        <circle cx="400" cy="300" r="60" fill="none" stroke="#3b82f6" stroke-width="1" opacity="0.8"/>
        
        <!-- Axis indicators -->
        <path d="M 100 300 L 700 300 M 400 50 L 400 550" stroke="#334155" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"/>
        <path d="M 120 280 L 120 320 M 680 280 L 680 320" stroke="#334155" stroke-width="1" opacity="0.5"/>
        
        <!-- Corner brackets -->
        <path d="M 30 50 L 30 30 L 50 30" fill="none" stroke="#6366f1" stroke-width="2" opacity="0.7"/>
        <path d="M 770 50 L 770 30 L 750 30" fill="none" stroke="#6366f1" stroke-width="2" opacity="0.7"/>
        <path d="M 30 550 L 30 570 L 50 570" fill="none" stroke="#6366f1" stroke-width="2" opacity="0.7"/>
        <path d="M 770 550 L 770 570 L 750 570" fill="none" stroke="#6366f1" stroke-width="2" opacity="0.7"/>
        
        <!-- Center Blueprint Card -->
        <rect x="200" y="210" width="400" height="180" rx="12" fill="#0f172a" fill-opacity="0.95" stroke="#3b82f6" stroke-width="2" style="filter: drop-shadow(0px 0px 20px rgba(59, 130, 246, 0.25));"/>
        
        <!-- Blueprint Text Details -->
        <text x="400" y="260" font-family="monospace" font-size="12" fill="#3b82f6" font-weight="bold" letter-spacing="4" text-anchor="middle">SCHEMATIC DIAGRAM</text>
        <text x="400" y="295" font-family="monospace" font-size="20" fill="#ffffff" font-weight="bold" text-anchor="middle">CONCEPTUAL MOCKUP</text>
        <text x="400" y="330" font-family="monospace" font-size="14" fill="#94a3b8" text-anchor="middle">{short_query}</text>
        <text x="400" y="360" font-family="monospace" font-size="11" fill="#f43f5e" font-weight="bold" text-anchor="middle">[ Rendering Server Offline - Schematic Fallback ]</text>
        
        <!-- CAD dimensions mock -->
        <text x="45" y="80" font-family="monospace" font-size="10" fill="#475569">SCALE: 1:1</text>
        <text x="45" y="100" font-family="monospace" font-size="10" fill="#475569">SYS_STATUS: ACTIVE</text>
        <text x="750" y="80" font-family="monospace" font-size="10" fill="#475569" text-anchor="end">REV: 2.1</text>
    </svg>"""
    img_str = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{img_str}"

async def generate_engineering_image(query: str) -> str:
    """
    Uses Pollinations.ai (Free, No API Key) as the primary generator (with retries).
    Falls back to Hugging Face InferenceClient if needed.
    If everything fails, returns a high-quality SVG CAD blueprint mockup.
    """
    prompt = f"A realistic, high-quality, modern engineering concept rendering of: {query}. Professional lighting, 3d CAD style."
    
    # 1. Primary: Pollinations AI with Retries
    for attempt in range(1, 4):
        try:
            print(f"Attempting image generation with Pollinations.ai (Attempt {attempt}/3)...")
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&width=1024&height=768"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=45.0)
                if response.status_code == 200:
                    img_str = base64.b64encode(response.content).decode("utf-8")
                    return f"data:image/jpeg;base64,{img_str}"
                else:
                    print(f"Pollinations AI attempt {attempt} failed with status: {response.status_code}")
        except Exception as e:
            print(f"Pollinations AI attempt {attempt} exception: {e}")
        
        # Short wait before retrying a queued IP
        if attempt < 3:
            await asyncio.sleep(2.0)
 
    # 2. Secondary Fallbacks: Hugging Face Free Tier
    if HF_TOKEN:
        print("Falling back to Hugging Face...")
        client = AsyncInferenceClient(api_key=HF_TOKEN, timeout=120.0)
        MODELS = [
            "stabilityai/stable-diffusion-xl-base-1.0",
            "black-forest-labs/FLUX.1-schnell",
            "runwayml/stable-diffusion-v1-5",
            "stabilityai/stable-diffusion-2-1",
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
                
    print("Error: All image generation engines failed. Serving fallback blueprint SVG mockup.")
    return get_fallback_svg(query)


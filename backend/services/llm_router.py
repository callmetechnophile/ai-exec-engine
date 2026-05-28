import os
import asyncio
from openai import AsyncOpenAI

# We set max_retries to 0 so the SDK doesn't waste time retrying a dead model.
_client = None

def get_client():
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ.get("NVIDIA_API_KEY"),
            max_retries=0, 
            timeout=15.0
        )
    return _client

# Prioritized list of reliable engineering-capable models on NVIDIA NIM
MODELS = [
    "meta/llama-3.1-70b-instruct",       # Primary: Smartest, but might queue
    "meta/llama-3.1-8b-instruct",        # Fallback 1: Extremely fast, rarely sleeps
    "google/gemma-2-27b-it",             # Fallback 2: Great logic/code
    "microsoft/phi-3-medium-4k-instruct" # Fallback 3: Solid reasoning
]

async def execute_prompt(prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
    """
    Executes a prompt against the primary model. If it fails or takes longer than 15 seconds,
    it automatically aborts and falls back to the next model in the list.
    """
    last_error = None
    
    for model in MODELS:
        try:
            print(f"[LLM Router] Attempting generation with {model}...")
            
            # Strict 15-second timeout per model
            response = await asyncio.wait_for(
                get_client().chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                ),
                timeout=15.0
            )
            
            print(f"[LLM Router] Success with {model}!")
            return response.choices[0].message.content.strip()
            
        except asyncio.TimeoutError:
            print(f"[LLM Router] {model} timed out after 15s. Failing over to next model.")
            last_error = "Timeout"
            continue
        except Exception as e:
            print(f"[LLM Router] {model} failed ({e}). Failing over to next model.")
            last_error = str(e)
            continue
            
    # If all models fail
    raise Exception(f"All fallback models exhausted. Last error: {last_error}")

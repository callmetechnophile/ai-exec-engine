import os
import asyncio
import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv("keys.env")

async def test_endpoints():
    print("Testing NVIDIA Llama 3.1 70B...")
    try:
        client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ.get("NVIDIA_API_KEY"),
            timeout=10.0
        )
        resp = await client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("Llama: OK", resp.choices[0].message.content)
    except Exception as e:
        print("Llama Failed:", type(e).__name__, str(e))

    print("\nTesting Tavily...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as http_client:
            payload = {
                "api_key": os.environ.get("TAVILY_API_KEY"),
                "query": "arduino robotics",
                "search_depth": "basic",
            }
            response = await http_client.post("https://api.tavily.com/search", json=payload)
            response.raise_for_status()
            print("Tavily: OK")
    except Exception as e:
        print("Tavily Failed:", type(e).__name__, str(e))

if __name__ == "__main__":
    asyncio.run(test_endpoints())

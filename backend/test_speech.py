import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        # Create a dummy small text file acting as audio
        files = {'file': ('test.webm', b'dummy audio data', 'audio/webm')}
        try:
            response = await client.post('http://localhost:8000/api/speech-to-text', files=files)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

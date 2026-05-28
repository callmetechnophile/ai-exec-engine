import httpx
import tempfile
import os

async def download_pdf(url: str) -> str:
    """
    Downloads a PDF from a URL and saves it to a temporary file.
    Returns the path to the downloaded PDF.
    """
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Create a temporary file
            fd, path = tempfile.mkstemp(suffix=".pdf")
            with os.fdopen(fd, 'wb') as f:
                f.write(response.content)
            return path
    except Exception as e:
        print(f"Error downloading PDF from {url}: {e}")
        return ""

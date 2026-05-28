import os
import httpx

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

async def search_projects(query: str) -> list:
    """
    Uses Tavily API to search for engineering projects, tutorials, and Hackster links.
    """
    if not TAVILY_API_KEY:
        print("Warning: TAVILY_API_KEY not set")
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"{query} engineering project tutorial Hackster github Instructables",
        "search_depth": "basic",
        "include_images": True,
        "max_results": 5
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            projects = []
            for result in data.get("results", []):
                # Try to extract a thumbnail if available
                thumbnail = None
                # Tavily includes images in a separate array, we'll just pick the first one if it exists
                # Or if result has image (depends on Tavily's exact image format)
                if data.get("images") and len(data.get("images")) > 0:
                     # very basic image assignment
                     thumbnail = data.get("images")[0]

                projects.append({
                    "title": result.get("title", "Unknown Title"),
                    "summary": result.get("content", "No summary available.")[:200] + "...",
                    "source": get_source_from_url(result.get("url", "")),
                    "url": result.get("url", ""),
                    "thumbnail": thumbnail
                })
            return projects
        except Exception as e:
            print(f"Error searching Tavily: {e}")
            return []

def get_source_from_url(url: str) -> str:
    if "github.com" in url:
        return "GitHub"
    elif "hackster.io" in url:
        return "Hackster"
    elif "instructables.com" in url:
        return "Instructables"
    elif "youtube.com" in url:
        return "YouTube"
    else:
        return "Web"

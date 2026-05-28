import os
import httpx
from services.pdf_service import download_pdf
from services.markdown_service import convert_pdf_to_markdown
from rag.chunking import chunk_markdown
from rag.embeddings import store_chunks
from services.llm_router import execute_prompt

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

async def retrieve_research_papers(query: str) -> list:
    """
    Uses Tavily API to search for academic research papers (arXiv, PubMed, etc.).
    """
    if not TAVILY_API_KEY:
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"{query} research paper academic arXiv PDF",
        "search_depth": "advanced",
        "max_results": 3
    }

    async with httpx.AsyncClient(timeout=120.0) as http_client:
        try:
            response = await http_client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for idx, result in enumerate(data.get("results", [])):
                paper_url = result.get("url", "")
                papers.append({
                    "id": f"paper_{idx}",
                    "title": result.get("title", "Unknown Title"),
                    "abstract": result.get("content", "No abstract available.")[:300] + "...",
                    "url": paper_url,
                    "source": "Tavily Retrieval"
                })
            return papers
        except Exception as e:
            print(f"Error fetching research: {e}")
            return []

async def process_paper_pdf(paper_url: str, paper_id: str):
    """
    Downloads PDF, converts to Markdown, chunks, and stores in RAG.
    Note: For MVP, we only process URLs ending in .pdf or known PDF hosts.
    """
    if not paper_url.endswith(".pdf"):
        # Very simple check for MVP, could be expanded
        return
        
    pdf_path = await download_pdf(paper_url)
    if pdf_path:
        md_text = convert_pdf_to_markdown(pdf_path)
        chunks = chunk_markdown(md_text)
        store_chunks(chunks, paper_id)

async def generate_engineering_insights(query: str, rag_context: str) -> list:
    """
    Uses Nemotron to generate insights based on the RAG context.
    """
    prompt = f"""
You are an expert engineering researcher. Based on the user query and the retrieved research context, provide 3-4 key engineering insights, methodologies, or architectural improvements.
Return ONLY a JSON array of strings, no markdown blocks or extra text.
Example: ["Insight 1", "Insight 2"]

User Query: {query}
Research Context:
{rag_context}
"""
    
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=512)
        import json
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except Exception as e:
        print(f"Error generating insights: {e}")
        return ["Could not generate insights at this time."]

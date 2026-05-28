import os
import math
from openai import OpenAI

# Use OpenAI for embeddings to save hundreds of MBs of RAM on Railway
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# Lightweight in-memory vector store for the MVP
MEMORY_DB = []

def get_embedding(text: str) -> list[float]:
    try:
        response = openai_client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def store_chunks(chunks: list[str], document_id: str):
    """
    Embeds and stores chunks in memory.
    """
    global MEMORY_DB
    if not chunks or not openai_client.api_key:
        return
        
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        if emb:
            MEMORY_DB.append({
                "id": f"{document_id}_{i}",
                "doc": chunk,
                "embedding": emb
            })

def query_context(query: str, n_results: int = 3) -> str:
    """
    Retrieves the most relevant chunks using pure cosine similarity.
    """
    global MEMORY_DB
    if not MEMORY_DB or not openai_client.api_key:
        return ""
        
    query_emb = get_embedding(query)
    if not query_emb:
        return ""
        
    def cosine_sim(a, b):
        dot = sum(x*y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x*x for x in a))
        norm_b = math.sqrt(sum(x*x for x in b))
        if norm_a == 0 or norm_b == 0: return 0
        return dot / (norm_a * norm_b)
        
    scored = []
    for item in MEMORY_DB:
        sim = cosine_sim(query_emb, item["embedding"])
        scored.append((sim, item["doc"]))
        
    scored.sort(key=lambda x: x[0], reverse=True)
    top_docs = [doc for sim, doc in scored[:n_results]]
    
    return "\n\n...\n\n".join(top_docs)

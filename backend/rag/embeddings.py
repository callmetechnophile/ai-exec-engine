import re

# Lightweight in-memory document store for the MVP
MEMORY_DB = []

def tokenize(text: str) -> set:
    return set(re.findall(r'\w+', text.lower()))

def store_chunks(chunks: list[str], document_id: str):
    """
    Stores chunks in memory.
    """
    global MEMORY_DB
    if not chunks:
        return
        
    for i, chunk in enumerate(chunks):
        MEMORY_DB.append({
            "id": f"{document_id}_{i}",
            "doc": chunk,
            "tokens": tokenize(chunk)
        })

def query_context(query: str, n_results: int = 3) -> str:
    """
    Retrieves the most relevant chunks using simple Jaccard similarity (word overlap).
    Zero dependencies, zero RAM bloat, zero API keys!
    """
    global MEMORY_DB
    if not MEMORY_DB:
        return ""
        
    query_tokens = tokenize(query)
    if not query_tokens:
        return ""
        
    def jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
        
    scored = []
    for item in MEMORY_DB:
        sim = jaccard_similarity(query_tokens, item["tokens"])
        scored.append((sim, item["doc"]))
        
    scored.sort(key=lambda x: x[0], reverse=True)
    top_docs = [doc for sim, doc in scored[:n_results]]
    
    return "\n\n...\n\n".join(top_docs)

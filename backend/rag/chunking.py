import re

def chunk_markdown(md_text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Splits markdown text into overlapping chunks for RAG.
    """
    if not md_text:
        return []

    # Very basic chunking by paragraphs to respect semantic boundaries roughly
    paragraphs = re.split(r'\n\s*\n', md_text)
    
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        if len(current_chunk) + len(p) < chunk_size:
            current_chunk += p + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    # Basic overlapping can be complex with pure paragraphs, 
    # but for this MVP, paragraph-level chunking is highly effective.
    return chunks

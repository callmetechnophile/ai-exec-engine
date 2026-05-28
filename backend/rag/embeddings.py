import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB in a local directory
chroma_client = chromadb.PersistentClient(path="./research_cache/chroma_db")
# Using a lightweight local embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def store_chunks(chunks: list[str], document_id: str):
    """
    Embeds and stores chunks in ChromaDB.
    """
    if not chunks:
        return
        
    collection = chroma_client.get_or_create_collection(name="engineering_research")
    
    embeddings = embedder.encode(chunks).tolist()
    
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"document_id": document_id} for _ in chunks]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

def query_context(query: str, n_results: int = 3) -> str:
    """
    Retrieves the most relevant chunks for a given query.
    """
    try:
        collection = chroma_client.get_collection(name="engineering_research")
        query_embedding = embedder.encode([query]).tolist()
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        if results and results['documents']:
            return "\n\n...\n\n".join(results['documents'][0])
        return ""
    except Exception as e:
        print(f"ChromaDB query error: {e}")
        return ""

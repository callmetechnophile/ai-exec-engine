import os
import chromadb
from chromadb.config import Settings

# Persistent local memory for Phase 4 engineering caching
MEMORY_DIR = os.path.join(os.path.dirname(__file__), "..", "memory")

client = chromadb.PersistentClient(path=MEMORY_DIR)
collection = client.get_or_create_collection(name="engineering_memory")

def cache_engineering_knowledge(query_id: str, knowledge_data: dict):
    import json
    collection.upsert(
        documents=[json.dumps(knowledge_data)],
        metadatas=[{"type": "engineering_execution"}],
        ids=[query_id]
    )

def retrieve_engineering_knowledge(query_id: str) -> dict:
    import json
    results = collection.get(ids=[query_id])
    if results and results.get("documents") and len(results["documents"]) > 0:
        try:
            return json.loads(results["documents"][0])
        except Exception:
            return None
    return None

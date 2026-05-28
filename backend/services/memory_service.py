import os
import json

# Persistent local memory for Phase 4 engineering caching
# Replacing ChromaDB with a simple lightweight disk cache to prevent OOM crashes
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "cache.json")

def _load_cache():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_cache(cache):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(cache, f)

def cache_engineering_knowledge(query_id: str, knowledge_data: dict):
    cache = _load_cache()
    cache[query_id] = knowledge_data
    _save_cache(cache)

def retrieve_engineering_knowledge(query_id: str) -> dict:
    cache = _load_cache()
    return cache.get(query_id, None)

from services.tavily_service import search_projects
from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    query = state["query"]
    state["logs"].append(f"[Retrieval Agent] Starting search for '{query}'")
    
    # Attempt 1
    projects = await search_projects(query)
    context = "".join([f"Title: {p['title']}\nSummary: {p['summary']}\n\n" for p in projects])
    
    # Evaluate sufficiency
    eval_prompt = f"""
    You are the Validation Sub-Agent. Does this context have enough engineering details to build: {query}?
    Context: {context}
    Return JSON: {{"sufficient": true/false, "new_query": "better search term if false"}}
    """
    try:
        content = await execute_prompt(eval_prompt, temperature=0.1, max_tokens=100)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        eval_data = json.loads(content)
        
        if not eval_data.get("sufficient", True):
            state["logs"].append(f"[Retrieval Agent] Context weak. Refining search: {eval_data.get('new_query')}")
            projects = await search_projects(eval_data.get("new_query", query + " engineering tutorial"))
    except Exception as e:
        state["logs"].append(f"[Retrieval Agent] Error evaluating context: {e}")

    state["retrieval_results"] = projects
    state["logs"].append("[Retrieval Agent] Retrieval complete.")
    return state

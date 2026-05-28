from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    query = state["query"]
    budget = state["budget"]
    context = "".join([f"{p['title']}: {p['summary']}\n" for p in state.get("retrieval_results", [])])
    
    state["logs"].append("[Extraction Agent] Extracting hardware/software components.")
    
    prompt = f"""
You are the Extraction Agent. Based on the query '{query}' and context below, extract the necessary engineering components.
Context: {context}
Target Budget: {budget}

Return ONLY JSON:
{{
    "engineering_components": [
        {{"name": "Component Name", "description": "Why it is needed", "estimated_price": 500, "category": "electronics/structural/software"}}
    ]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=1024)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["engineering_components"] = data.get("engineering_components", [])
    except Exception as e:
        state["logs"].append(f"[Extraction Agent] Error extracting components: {e}")
        state["engineering_components"] = []

    state["logs"].append(f"[Extraction Agent] Extracted {len(state['engineering_components'])} components.")
    return state

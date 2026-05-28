import json
from services.llm_router import execute_prompt

async def evaluate_research_sufficiency(query: str, current_context: str) -> dict:
    """
    Evaluates if the current retrieved context has enough engineering depth.
    """
    prompt = f"""
You are an autonomous engineering agent. Read the user's project query and the currently retrieved research context.
Determine if the context contains sufficient actionable engineering data (e.g. specific components, wiring, algorithms) to build the project.

User Query: {query}
Current Context:
{current_context}

Respond ONLY with a JSON object in this format:
{{
    "is_sufficient": true/false,
    "reason": "Brief explanation",
    "suggested_new_query": "A more specific or alternative search query if insufficient"
}}
"""
    try:
        content = await execute_prompt(prompt, temperature=0.1, max_tokens=256)
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except Exception as e:
        print(f"Error evaluating research: {e}")
        # Default to sufficient to prevent infinite loops on error
        return {"is_sufficient": True, "reason": "Error parsing", "suggested_new_query": ""}

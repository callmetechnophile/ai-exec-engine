from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    state["logs"].append("[Research Agent] Analyzing technical approaches.")
    
    components = [c.get("name") for c in state.get("engineering_components", [])]
    
    prompt = f"""
You are the Research Agent. Based on the components {components} for the project '{state['query']}', extract 3 critical engineering insights or methodologies required for successful assembly.
Return ONLY JSON:
{{
    "research_insights": ["Insight 1", "Insight 2", "Insight 3"]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.3, max_tokens=512)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["research_insights"] = data.get("research_insights", [])
    except Exception as e:
        state["logs"].append(f"[Research Agent] Error extracting insights: {e}")
        state["research_insights"] = []

    state["logs"].append("[Research Agent] Research insights generated.")
    return state

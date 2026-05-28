from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    state["logs"].append("[Validation Agent] Validating architecture for contradictions.")
    
    components_str = json.dumps(state.get("engineering_components", []))
    opts = json.dumps(state.get("optimization_recommendations", []))
    
    prompt = f"""
You are the Validation Agent. Analyze the architecture for '{state['query']}'.
Components: {components_str}
Proposed Optimizations: {opts}

Detect any impossible configurations, contradictory requirements, or feasibility alerts (e.g., motor requires 5A but battery provides 1A).
Return ONLY JSON:
{{
    "validation_warnings": ["Warning 1", "Alert 2"]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.1, max_tokens=256)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["validation_warnings"] = data.get("validation_warnings", [])
    except Exception as e:
        state["logs"].append(f"[Validation Agent] Error validating: {e}")
        state["validation_warnings"] = []

    state["logs"].append(f"[Validation Agent] Validation complete. {len(state['validation_warnings'])} warnings found.")
    return state

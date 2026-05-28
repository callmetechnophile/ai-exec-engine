from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    state["logs"].append("[Optimization Agent] Optimizing components for budget and complexity.")
    
    components_str = json.dumps(state.get("engineering_components", []))
    
    prompt = f"""
You are the Optimization Agent. The user wants to build '{state['query']}' with complexity '{state['complexity']}' and budget ₹{state['budget']}.
Current components: {components_str}

Suggest 2-3 cheaper or more appropriate alternative components.
Return ONLY JSON:
{{
    "optimization_recommendations": [
        {{"original": "Component A", "alternative": "Component B", "reason": "Better for this complexity/budget"}}
    ]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=512)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["optimization_recommendations"] = data.get("optimization_recommendations", [])
    except Exception as e:
        state["logs"].append(f"[Optimization Agent] Error generating optimizations: {e}")
        state["optimization_recommendations"] = []

    state["logs"].append("[Optimization Agent] Optimizations generated.")
    return state

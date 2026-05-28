from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    state["logs"].append("[Deployment Agent] Generating deployment intelligence.")
    
    components = json.dumps(state.get("engineering_components", []))
    
    prompt = f"""
You are the Deployment Agent. Analyze the architecture for '{state['query']}'.
Components: {components}

Generate 2-3 deployment recommendations for scaling or moving this project into a production environment.
Return ONLY JSON:
{{
    "deployment_recommendations": ["Recommendation 1", "Recommendation 2"]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.3, max_tokens=256)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["deployment_recommendations"] = data.get("deployment_recommendations", [])
    except Exception as e:
        state["logs"].append(f"[Deployment Agent] Error: {e}")
        state["deployment_recommendations"] = []

    state["logs"].append("[Deployment Agent] Deployment intelligence generated.")
    return state

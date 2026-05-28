from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    state["logs"].append("[Simulation Agent] Running feasibility & bottleneck simulation.")
    
    components = json.dumps(state.get("engineering_components", []))
    warnings = json.dumps(state.get("validation_warnings", []))
    
    prompt = f"""
You are the Simulation Agent. Your task is to perform an AI-assisted feasibility simulation.
Project: '{state['query']}'
Components: {components}
Current Warnings: {warnings}

Simulate the execution and runtime of this project. Identify 1-2 potential physical bottlenecks or feasibility risks (e.g., 'Motor overheating risk after extended runtime').
Return ONLY JSON:
{{
    "simulation_results": ["Bottleneck 1", "Feasibility issue 2"]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=256)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["simulation_results"] = data.get("simulation_results", [])
    except Exception as e:
        state["logs"].append(f"[Simulation Agent] Error during simulation: {e}")
        state["simulation_results"] = []

    state["logs"].append(f"[Simulation Agent] Simulation complete. Found {len(state['simulation_results'])} bottlenecks.")
    return state

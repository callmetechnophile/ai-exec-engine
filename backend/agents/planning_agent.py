from services.llm_router import execute_prompt
import json

async def run(state: dict) -> dict:
    state["logs"].append("[Planning Agent] Generating execution plan and score.")
    
    warnings_count = len(state.get("validation_warnings", []))
    components_count = len(state.get("engineering_components", []))
    
    prompt = f"""
You are the Planning Agent. The project is '{state['query']}' with {components_count} components.
Warnings found: {warnings_count}
Timeframe: {state['time']}

1. Generate 3-5 sequential Gantt tasks.
2. Calculate an execution readiness score (0-100). Subtract points for warnings.

Return ONLY JSON:
{{
    "execution_score": 85,
    "execution_plan": ["Phase 1: Setup", "Phase 2: Build"],
    "gantt_tasks": [
        {{"id": "T1", "name": "Task 1", "start": "2026-05-28", "end": "2026-05-30", "dependencies": ""}}
    ]
}}
    """
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=512)
        if "```json" in content: content = content.split("```json")[1].split("```")[0]
        elif "```" in content: content = content.split("```")[1].split("```")[0]
        data = json.loads(content)
        state["execution_score"] = data.get("execution_score", 70)
        state["execution_plan"] = data.get("execution_plan", [])
        state["gantt_tasks"] = data.get("gantt_tasks", [])
    except Exception as e:
        state["logs"].append(f"[Planning Agent] Error generating plan: {e}")
        state["execution_score"] = 50
        state["execution_plan"] = []
        state["gantt_tasks"] = []

    state["logs"].append("[Planning Agent] Execution plan ready.")
    return state

import json
from services.llm_router import execute_prompt

async def calculate_readiness_score(query: str, components: list, budget: int, complexity: str) -> int:
    """
    Analyzes project realism and returns a readiness score (0-100).
    """
    prompt = f"""
You are a strict engineering project auditor. Evaluate the readiness/feasibility of this project based on:
- Complexity vs Budget realism
- Availability of required components

Project: {query}
Target Budget: ₹{budget}
Target Complexity: {complexity}
Components: {json.dumps([c.get('name') for c in components])}

Calculate a score from 0 to 100. Be realistic. If a budget is too low for the complexity, lower the score.
Respond ONLY with a JSON object in this format:
{{
    "execution_score": 85
}}
"""
    try:
        content = await execute_prompt(prompt, temperature=0.1, max_tokens=100)
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        data = json.loads(content)
        return int(data.get("execution_score", 50))
    except Exception as e:
        print(f"Error calculating score: {e}")
        return 50

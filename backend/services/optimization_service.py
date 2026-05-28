import os
import json
from services.llm_router import execute_prompt

async def optimize_components(components: list, budget: int, complexity: str, time: str) -> list:
    """
    Uses Nemotron to optimize components based on Complexity -> Budget -> Time priority.
    """
    if not components:
        return []
        
    prompt = f"""
You are an expert engineering optimizer. Review the following project components.
Optimization Priority: 1. {complexity} Complexity constraints 2. Fit within {budget} budget 3. Fit within {time} timeline.
Suggest improved alternatives or upgrades.

Components: {json.dumps(components)}

Respond ONLY with a JSON array in the following format:
[
  {{"name": "Upgraded Component Name", "description": "Why it was upgraded (e.g. Replace L298N with BTS7960 for higher efficiency)", "estimated_price": 60.0}}
]
"""
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=1024)
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except Exception as e:
        print(f"Error optimizing components: {e}")
        return components

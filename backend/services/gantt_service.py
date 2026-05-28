import os
import json
from services.llm_router import execute_prompt

async def generate_gantt_tasks(query: str, time_constraint: str) -> list:
    """
    Uses Gemma to generate a project roadmap matching frappe-gantt's structure.
    """
    prompt = f"""
You are an expert engineering project manager. Create a timeline for: {query}
Total time allowed: {time_constraint}

Output a JSON array of tasks compatible with frappe-gantt. Format:
[
  {{
    "id": "Task 1",
    "name": "Research and Design",
    "start": "2026-06-01",
    "end": "2026-06-05",
    "progress": 0,
    "dependencies": ""
  }}
]
Ensure dates logically flow and fit within {time_constraint}. Use YYYY-MM-DD.
"""
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=1024)
        
        # Robustly extract JSON array
        start_idx = content.find("[")
        end_idx = content.rfind("]")
        if start_idx != -1 and end_idx != -1:
            content = content[start_idx:end_idx+1]
            
        return json.loads(content)
    except Exception as e:
        print(f"Error generating gantt tasks: {e}")
        return []

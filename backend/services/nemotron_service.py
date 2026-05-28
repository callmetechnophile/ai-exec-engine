import os
import json
from services.llm_router import execute_prompt

async def extract_components(query: str, project_context: str) -> dict:
    prompt = f"""
You are an expert engineering assistant. Based on the user query and the retrieved project context, extract the required engineering components.
Categorize them into 'electronics', 'structural', 'mechanical', 'pneumatic', and 'fluid_power'.
If a category has no components, leave its list empty.
Do not hallucinate components that aren't typically needed for such a project.

Respond ONLY with a JSON object in the following format, with no additional text or markdown formatting:
{{
  "electronics": [
    {{"name": "Component Name", "description": "Short description", "estimated_price": 50.0}}
  ],
  "structural": [],
  "mechanical": [],
  "pneumatic": [],
  "fluid_power": []
}}

User Query: {query}
Project Context (Summaries from web search):
{project_context}
"""
    
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=1024)
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing Nemotron response: {e}")
        return {
            "electronics": [],
            "structural": [],
            "mechanical": [],
            "pneumatic": [],
            "fluid_power": []
        }

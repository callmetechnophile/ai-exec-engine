import os
import json
from services.llm_router import execute_prompt

async def extract_project_info(query: str) -> dict:
    prompt = f"""
You are an expert engineering assistant. Analyze the following user query and extract the project information.
Respond ONLY with a JSON object in the following format, with no additional text or formatting:
{{
  "project_name": "Name of the project",
  "domain": "Domain (e.g., Robotics, IoT, Automotive)",
  "difficulty": "Difficulty level (e.g., Beginner, Intermediate, Advanced)"
}}

User Query: {query}
"""
    
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=256)
        if content.startswith("```json"):
            content = content[7:-3]
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing Gemma response: {e}")
        return {
            "project_name": "Unknown Project",
            "domain": "General Engineering",
            "difficulty": "Unknown"
        }

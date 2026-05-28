import json
from services.llm_router import execute_prompt

async def analyze_execution_architecture(query: str, components: list) -> dict:
    """
    Generates alternative components, implementation advice, and hidden risks.
    """
    prompt = f"""
You are a Principal Hardware Engineer. Analyze the proposed project architecture.
Project: {query}
Current Components: {json.dumps([c.get('name') for c in components])}

Generate:
1. 3 engineering recommendations (advice, future scalability).
2. 3 research/hidden insights (risks, dependency warnings).
3. 2-3 alternative components (e.g. replacing L298N with BTS7960) with advantages.
4. A list of 3-5 high-level steps representing the critical path for assembly.

Respond ONLY with a JSON object in this exact format:
{{
    "engineering_recommendations": ["Rec 1", "Rec 2"],
    "research_insights": ["Insight 1", "Warning 2"],
    "alternative_components": [
        {{"component": "Original", "alternative": "New", "advantage": "Reason"}}
    ],
    "critical_path": ["Step 1", "Step 2", "Step 3"]
}}
"""
    try:
        content = await execute_prompt(prompt, temperature=0.3, max_tokens=1024)
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
        return json.loads(content)
    except Exception as e:
        print(f"Error in execution analysis: {e}")
        return {
            "engineering_recommendations": [],
            "research_insights": [],
            "alternative_components": [],
            "critical_path": []
        }

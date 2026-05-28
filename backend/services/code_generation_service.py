import os
import json
from services.llm_router import execute_prompt

async def generate_microcontroller_code(query: str, components: list, mcu_type: str) -> str:
    """
    Uses Llama 3 to generate starter code for a specific microcontroller.
    """
    prompt = f"""
You are an expert embedded software engineer. Provide clean, modular starter code for the following project: {query}.
The target microcontroller is: {mcu_type}.
Components involved: {json.dumps([c.get('name') for c in components])}

Do NOT hallucinate hardware pin mappings, use defined constants.
Respond ONLY with the actual code block. Do NOT wrap it in markdown formatting like ```c or ```python.
Just provide the raw code text.
"""
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=2048)
        
        # Cleanup in case the LLM ignored instructions and included markdown
        if content.startswith("```"):
            lines = content.split('\n')
            if len(lines) > 2 and lines[-1].startswith("```"):
                content = '\n'.join(lines[1:-1])
                
        return content
    except Exception as e:
        print(f"Error generating code: {e}")
        return f"// Error generating code for {mcu_type}"

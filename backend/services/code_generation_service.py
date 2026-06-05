import os
import json
from services.llm_router import execute_prompt

async def generate_microcontroller_code(query: str, components: list, mcu_type: str) -> str:
    """
    Uses Groq/Llama 3 to generate actual functional connection and control code for a specific microcontroller.
    """
    # Create a descriptive list of components to feed into the prompt
    components_info = []
    for c in components:
        name = c.get("name", "Unknown Component")
        desc = c.get("description", "")
        components_info.append(f"- {name}: {desc}")
    components_str = "\n".join(components_info)

    prompt = f"""
You are an expert embedded software engineer. Provide complete, fully functional, and actual implementation code (not generic boilerplate or empty placeholder comments) for the following project:
Project Goal: {query}
Target Microcontroller: {mcu_type}

List of Optimized Components & Details to Connect:
{components_str}

Instructions:
1. Define a clear, realistic physical pin mapping table in the initial comments of the code showing exactly how each component connects to the target microcontroller ({mcu_type}).
2. Use concrete GPIO, analog, digital, or communications (SDA/SCL, TX/RX, SPI) pin assignments appropriate for {mcu_type}. Do not use empty placeholders; define actual numeric constants (e.g. '#define MOTOR_IN1_PIN 4' or 'const int sensorPin = 34').
3. Implement full, actual driver/connection logic in the setup() and main execution loop/function. Write the code to read from sensors, write output control signals to actuators, handle timers, and coordinate interaction between the components.
4. Include standard initialization protocols (e.g. Serial.begin, Wire.begin, pinModes, servo attachments) and control loops.
5. Return ONLY the raw code text block. Do NOT wrap it in markdown block quotes like ```c, ```cpp, or ```python.
"""
    try:
        content = await execute_prompt(prompt, temperature=0.2, max_tokens=2048)
        
        # Cleanup in case the LLM ignored instructions and included markdown
        content_stripped = content.strip()
        if content_stripped.startswith("```"):
            lines = content_stripped.split('\n')
            if len(lines) > 2 and lines[-1].startswith("```"):
                # strip out the language identifier (e.g. ```cpp) and ending ```
                content_stripped = '\n'.join(lines[1:-1])
        return content_stripped
    except Exception as e:
        print(f"Error generating code: {e}")
        return f"// Error generating code for {mcu_type}"


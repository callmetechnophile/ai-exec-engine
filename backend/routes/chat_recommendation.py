from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from services.llm_service import call_nvidia_nim

router = APIRouter()

class ChatRecommendationRequest(BaseModel):
    message: str
    context: dict

@router.post("/chat-recommendation")
async def chat_recommendation(req: ChatRecommendationRequest):
    try:
        system_prompt = f"""You are a senior engineering consultant AI.
The user is asking about an alternative component, architecture, or feasibility question regarding their engineering project.

CRITICAL INSTRUCTION:
You MUST format your response by strictly outputting a probabilistic credibility score on the first line (e.g., 'Probability of Success: 82%').
Then, provide a strict engineering reason for that probability. Keep it concise, analytical, and highly professional.

Context of their current project (Budget, Complexity, Chosen Components, Recommendations):
{json.dumps(req.context)}
"""
        response = call_nvidia_nim([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message}
        ])
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

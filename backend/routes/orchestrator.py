from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.agent_orchestrator import start_pipeline, get_pipeline_status

router = APIRouter()

class OrchestratorRequest(BaseModel):
    query: str
    budget: int
    complexity: str
    time: str

@router.post("/start-orchestrator")
async def start_orch(req: OrchestratorRequest):
    task_id = start_pipeline(req.query, req.budget, req.complexity, req.time)
    return {"task_id": task_id}

@router.get("/orchestrator-status/{task_id}")
async def get_status(task_id: str):
    state = get_pipeline_status(task_id)
    if state.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Task not found")
    return state

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.workspace_service import get_all_workspaces, load_workspace
from services.agent_orchestrator import iterate_pipeline, load_active_pipeline

router = APIRouter()

@router.get("/workspaces")
async def list_workspaces():
    return get_all_workspaces()

@router.get("/workspace/{workspace_id}")
async def get_workspace(workspace_id: str):
    data = load_workspace(workspace_id)
    if not data:
        raise HTTPException(status_code=404, detail="Workspace not found")
    load_active_pipeline(workspace_id, data) # Loads it back into memory so polling works
    return data

class IterateRequest(BaseModel):
    budget: int
    complexity: str
    time: str

@router.post("/workspace/{workspace_id}/iterate")
async def iterate_workspace(workspace_id: str, req: IterateRequest):
    data = load_workspace(workspace_id)
    if not data:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Must ensure it's in memory before iterating
    load_active_pipeline(workspace_id, data)
    task_id = iterate_pipeline(workspace_id, req.budget, req.complexity, req.time)
    
    return {"task_id": task_id}

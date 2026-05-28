from copy import deepcopy
from datetime import datetime
from services.workspace_service import save_workspace

def fork_version(state: dict, new_budget: int, new_complexity: str) -> dict:
    # Save the current state into the versions history
    old_state = deepcopy(state)
    
    # Clean up massive fields from the historic version so the JSON doesn't bloat
    if "logs" in old_state:
        del old_state["logs"]
    
    old_state["version_date"] = datetime.now().isoformat()
    
    if "versions" not in state:
        state["versions"] = []
    
    # Store the old version
    state["versions"].append(old_state)
    
    # Update current parameters
    state["budget"] = new_budget
    state["complexity"] = new_complexity
    state["logs"] = [f"[Versioning] Iterated from version {len(state['versions'])}. Budget: {new_budget}"]
    state["status"] = "RUNNING"
    state["current_agent"] = "Initializing Iteration"
    
    # Note: Retrieval/Extraction results remain in state, so we save LLM tokens!
    return state

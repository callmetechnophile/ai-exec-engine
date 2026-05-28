import os
import json
import uuid
from datetime import datetime

WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "..", "workspaces")

def create_workspace(state: dict) -> str:
    workspace_id = str(uuid.uuid4())
    state["workspace_id"] = workspace_id
    state["created_at"] = datetime.now().isoformat()
    state["versions"] = [] # to hold older states
    save_workspace(workspace_id, state)
    return workspace_id

def save_workspace(workspace_id: str, state: dict):
    filepath = os.path.join(WORKSPACE_DIR, f"{workspace_id}.json")
    with open(filepath, "w") as f:
        json.dump(state, f, indent=4)

def load_workspace(workspace_id: str) -> dict:
    filepath = os.path.join(WORKSPACE_DIR, f"{workspace_id}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)

def get_all_workspaces() -> list:
    workspaces = []
    if not os.path.exists(WORKSPACE_DIR):
        return workspaces
    for filename in os.listdir(WORKSPACE_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(WORKSPACE_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    workspaces.append({
                        "id": data.get("workspace_id"),
                        "query": data.get("query"),
                        "created_at": data.get("created_at"),
                        "health": data.get("execution_score", 0)
                    })
            except Exception:
                continue
    return sorted(workspaces, key=lambda x: x["created_at"], reverse=True)

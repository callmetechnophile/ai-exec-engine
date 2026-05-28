import json
import os

EXECUTION_LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "execution_logs")

def update_task_progress(workspace_id: str, task_id: str, completed: bool):
    # In a real database, we'd update a boolean. Here we just store completion IDs
    log_path = os.path.join(EXECUTION_LOGS_DIR, f"{workspace_id}_tasks.json")
    
    completed_tasks = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            completed_tasks = json.load(f)
            
    if completed and task_id not in completed_tasks:
        completed_tasks.append(task_id)
    elif not completed and task_id in completed_tasks:
        completed_tasks.remove(task_id)
        
    with open(log_path, "w") as f:
        json.dump(completed_tasks, f)
        
    return completed_tasks

def get_task_progress(workspace_id: str) -> list:
    log_path = os.path.join(EXECUTION_LOGS_DIR, f"{workspace_id}_tasks.json")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return json.load(f)
    return []

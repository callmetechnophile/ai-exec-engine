import asyncio
import uuid
import time
from agents import retrieval_agent, extraction_agent, research_agent, optimization_agent, validation_agent, planning_agent, simulation_agent, deployment_agent
from services.memory_service import cache_engineering_knowledge, retrieve_engineering_knowledge
from services.workspace_service import create_workspace, save_workspace
from services.decision_trace_service import generate_decision_trace
from services.versioning_service import fork_version
from services.export_service import generate_exports

active_pipelines = {}

async def run_pipeline(task_id: str, query: str, budget: int, complexity: str, time_constraint: str, existing_workspace_id: str = None):
    """
    Executes the multi-agent engineering pipeline autonomously.
    
    This function acts as the central orchestrator, passing the project state
    sequentially through the retrieval, extraction, research, optimization, 
    validation, simulation, deployment, and planning agents.
    
    Args:
        task_id (str): Unique identifier for the orchestration task.
        query (str): User's engineering project prompt.
        budget (int): Maximum budget constraint in INR.
        complexity (str): Desired complexity level (Easy, Medium, Hard).
        time_constraint (str): Time constraint for the project.
        existing_workspace_id (str, optional): ID of an existing workspace to iterate on, if any.
    """
    
    if existing_workspace_id and existing_workspace_id in active_pipelines:
        state = active_pipelines[existing_workspace_id]
        state = fork_version(state, budget, complexity)
        task_id = existing_workspace_id # keep using the same ID
    else:
        state = {
            "query": query,
            "budget": budget,
            "complexity": complexity,
            "time": time_constraint,
            "retrieval_results": [],
            "engineering_components": [],
            "research_insights": [],
            "optimization_recommendations": [],
            "validation_warnings": [],
            "simulation_results": [],
            "deployment_recommendations": [],
            "decision_trace": [],
            "execution_plan": [],
            "gantt_tasks": [],
            "execution_score": 0,
            "current_agent": "Initializing",
            "status": "RUNNING",
            "logs": [],
            "versions": []
        }
        
    active_pipelines[task_id] = state
    
    try:
        if not existing_workspace_id:
            cached_data = retrieve_engineering_knowledge(query)
            if cached_data:
                state["logs"].append("[Memory Store] Found cached engineering knowledge. Fast-forwarding retrieval.")
                state["retrieval_results"] = cached_data.get("retrieval_results", [])
                state["engineering_components"] = cached_data.get("engineering_components", [])
            else:
                state["current_agent"] = "Retrieval Agent"
                state = await retrieval_agent.run(state)
                
                state["current_agent"] = "Extraction Agent"
                state = await extraction_agent.run(state)
                
                cache_engineering_knowledge(query, {
                    "retrieval_results": state["retrieval_results"],
                    "engineering_components": state["engineering_components"]
                })

            state["current_agent"] = "Research Agent"
            state = await research_agent.run(state)
        
        state["current_agent"] = "Optimization Agent"
        state = await optimization_agent.run(state)
        
        state["current_agent"] = "Validation Agent"
        state = await validation_agent.run(state)
        
        state["current_agent"] = "Simulation Agent"
        state = await simulation_agent.run(state)
        
        state["current_agent"] = "Deployment Agent"
        state = await deployment_agent.run(state)
        
        state["current_agent"] = "Planning Agent"
        state = await planning_agent.run(state)
        
        state["decision_trace"] = generate_decision_trace(state)
        
        state["current_agent"] = "Complete"
        state["status"] = "DONE"
        
        # Generate export files and attach their paths to the state
        try:
            export_paths = generate_exports(state)
            state.update(export_paths)
            state["logs"].append("[Orchestrator] Generated export documents successfully.")
        except Exception as ex:
            state["logs"].append(f"[Orchestrator] Failed to generate exports: {ex}")
        
        if existing_workspace_id:
            save_workspace(task_id, state)
        else:
            state["workspace_id"] = task_id
            create_workspace(state)
            
    except Exception as e:
        state["status"] = "ERROR"
        state["logs"].append(f"[Orchestrator] Pipeline crashed: {e}")
        
    active_pipelines[task_id] = state

def start_pipeline(query: str, budget: int, complexity: str, time: str) -> str:
    task_id = str(uuid.uuid4())
    asyncio.create_task(run_pipeline(task_id, query, budget, complexity, time))
    return task_id

def iterate_pipeline(workspace_id: str, budget: int, complexity: str, time: str) -> str:
    asyncio.create_task(run_pipeline(workspace_id, "", budget, complexity, time, existing_workspace_id=workspace_id))
    return workspace_id

def get_pipeline_status(task_id: str) -> dict:
    return active_pipelines.get(task_id, {"status": "NOT_FOUND"})

def load_active_pipeline(workspace_id: str, state: dict):
    active_pipelines[workspace_id] = state

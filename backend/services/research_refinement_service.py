from services.agentic_service import evaluate_research_sufficiency
from services.tavily_service import search_projects

async def perform_agentic_research(initial_query: str, max_retries: int = 1) -> tuple[list, str, list]:
    """
    Executes an autonomous research loop.
    Returns: (projects, final_context, refinement_logs)
    """
    current_query = initial_query
    all_projects = []
    context = ""
    logs = []
    
    for attempt in range(max_retries + 1):
        logs.append(f"Attempt {attempt + 1}: Searching for '{current_query}'...")
        
        projects = await search_projects(current_query)
        
        # Build context to evaluate
        new_context = ""
        for p in projects:
            new_context += f"Title: {p['title']}\nSummary: {p['summary']}\n\n"
        
        all_projects.extend(projects)
        context += new_context
        
        if attempt == max_retries:
            logs.append("Max research iterations reached.")
            break
            
        evaluation = await evaluate_research_sufficiency(initial_query, context)
        
        if evaluation.get("is_sufficient", True):
            logs.append("Research context deemed sufficient by AI agent.")
            break
        else:
            reason = evaluation.get("reason", "Unknown")
            next_query = evaluation.get("suggested_new_query", initial_query + " tutorial hackster")
            logs.append(f"Research insufficient. Reason: {reason}. Refining query to: '{next_query}'")
            current_query = next_query
            
    # Deduplicate projects by URL
    unique_projects = {p['url']: p for p in all_projects}.values()
    return list(unique_projects), context, logs

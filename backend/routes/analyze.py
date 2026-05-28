from fastapi import APIRouter, HTTPException
from models.schemas import ProjectQuery, AnalysisResponse, ProjectInfo
from services.tavily_service import search_projects
from services.nemotron_service import extract_components
from services.gemma_service import extract_project_info
import asyncio

router = APIRouter()

@router.post("/analyze-project", response_model=AnalysisResponse)
async def analyze_project(query: ProjectQuery):
    try:
        # Step 1 & 2: Extract project info and search web concurrently
        print(f"[Analyze] Starting Gemma & Tavily extraction for: {query.query}")
        
        info_task = asyncio.create_task(extract_project_info(query.query))
        search_task = asyncio.create_task(search_projects(query.query))
        
        project_info_data = await info_task
        project_info = ProjectInfo(**project_info_data)
        
        projects = await search_task
        print(f"[Analyze] Extraction & Search completed, found {len(projects)} projects")

        # Build context for Nemotron from search results
        context = ""
        for p in projects:
            context += f"Title: {p['title']}\nSummary: {p['summary']}\n\n"

        # Step 3: Extract components using Nemotron
        print(f"[Analyze] Starting Nemotron component extraction")
        components_data = await extract_components(query.query, context)
        print(f"[Analyze] Nemotron completed successfully")

        # Assemble final response
        response = AnalysisResponse(
            project_info=project_info,
            projects=projects,
            electronics=components_data.get("electronics", []),
            structural=components_data.get("structural", []),
            mechanical=components_data.get("mechanical", []),
            pneumatic=components_data.get("pneumatic", []),
            fluid_power=components_data.get("fluid_power", [])
        )
        return response


    except Exception as e:
        print(f"[Analyze] Error in analyze-project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

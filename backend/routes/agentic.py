from fastapi import APIRouter, HTTPException
import asyncio
from models.schemas import ExecutionRequest, ExecutionPackageResponse
from services.research_refinement_service import perform_agentic_research
from services.scoring_service import calculate_readiness_score
from services.execution_analysis_service import analyze_execution_architecture
from services.optimization_service import optimize_components
from services.gantt_service import generate_gantt_tasks
from services.fal_service import generate_engineering_image
from services.export_service import generate_exports

router = APIRouter()

@router.post("/generate-execution-package", response_model=ExecutionPackageResponse)
async def generate_execution_package(req: ExecutionRequest):
    try:
        # 1. Agentic Research Loop
        print("[Agentic] Starting research loop...")
        research_projects, research_context, logs = await perform_agentic_research(req.query, max_retries=1)
        
        # 2. Concurrently run all analysis and generation services
        print("[Agentic] Spawning parallel analysis tasks...")
        score_task = asyncio.create_task(calculate_readiness_score(req.query, req.components, req.budget, req.complexity))
        analysis_task = asyncio.create_task(analyze_execution_architecture(req.query, req.components))
        opt_task = asyncio.create_task(optimize_components(req.components, req.budget, req.complexity, req.time))
        gantt_task = asyncio.create_task(generate_gantt_tasks(req.query, req.time))
        image_task = asyncio.create_task(generate_engineering_image(req.query))
        
        # Await all
        execution_score = await score_task
        analysis_data = await analysis_task
        optimized_comps = await opt_task
        gantt_tasks = await gantt_task
        image_url = await image_task
        
        # 3. Aggregate
        package_data = {
            "execution_score": execution_score,
            "optimized_components": optimized_comps,
            "engineering_recommendations": analysis_data.get("engineering_recommendations", []),
            "research_insights": logs + analysis_data.get("research_insights", []),
            "alternative_components": analysis_data.get("alternative_components", []),
            "critical_path": analysis_data.get("critical_path", []),
            "gantt_tasks": gantt_tasks,
            "generated_visualization": image_url
        }
        
        # 4. Generate Export Files
        print("[Agentic] Generating export files...")
        export_paths = generate_exports(package_data)
        
        return ExecutionPackageResponse(
            **package_data,
            **export_paths
        )
        
    except Exception as e:
        print(f"[Agentic] Error generating package: {e}")
        raise HTTPException(status_code=500, detail=str(e))

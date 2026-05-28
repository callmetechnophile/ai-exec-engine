from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio

from services.research_service import retrieve_research_papers, process_paper_pdf, generate_engineering_insights
from services.optimization_service import optimize_components
from services.code_generation_service import generate_microcontroller_code
from services.gantt_service import generate_gantt_tasks
from services.fal_service import generate_engineering_image
from services.export_service import generate_csv_export
from rag.embeddings import query_context

router = APIRouter()

class AdvanceRequest(BaseModel):
    query: str
    components: List[Dict[str, Any]]
    budget: int
    complexity: str
    time: str

class AdvanceResponse(BaseModel):
    research_papers: List[Dict[str, Any]]
    engineering_insights: List[str]
    optimized_components: List[Dict[str, Any]]
    gantt_tasks: List[Dict[str, Any]]
    generated_image: str
    csv_export: str

@router.post("/advance-research", response_model=AdvanceResponse)
async def advance_research(req: AdvanceRequest):
    try:
        # 1. Start long-running independent tasks
        image_task = asyncio.create_task(generate_engineering_image(req.query))
        gantt_task = asyncio.create_task(generate_gantt_tasks(req.query, req.time))
        opt_task = asyncio.create_task(optimize_components(req.components, req.budget, req.complexity, req.time))
        
        # 2. Sequential RAG pipeline
        papers = await retrieve_research_papers(req.query)
        
        # In a real MVP, we'd process all papers concurrently, but let's process the first PDF to avoid timeouts
        if papers and len(papers) > 0:
            # We just process the first one that has a .pdf for speed in this demo
            for p in papers:
                if p["url"].endswith(".pdf"):
                    await process_paper_pdf(p["url"], p["id"])
                    break
        
        # Query ChromaDB context
        context = query_context(req.query, n_results=3)
        
        # Generate insights based on RAG
        insights = await generate_engineering_insights(req.query, context)
        
        # 3. Await all independent tasks
        image_url = await image_task
        gantt_data = await gantt_task
        optimized_comps = await opt_task
        
        # 4. Generate CSV
        csv_data = generate_csv_export(gantt_data)
        
        return AdvanceResponse(
            research_papers=papers,
            engineering_insights=insights,
            optimized_components=optimized_comps,
            gantt_tasks=gantt_data,
            generated_image=image_url,
            csv_export=csv_data
        )
        
    except Exception as e:
        print(f"Error in advance-research: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class GenerateCodeRequest(BaseModel):
    query: str
    components: List[Dict[str, Any]]
    mcu_type: str

class GenerateCodeResponse(BaseModel):
    code: str

@router.post("/generate-code", response_model=GenerateCodeResponse)
async def generate_code(req: GenerateCodeRequest):
    try:
        code = await generate_microcontroller_code(req.query, req.components, req.mcu_type)
        return GenerateCodeResponse(code=code)
    except Exception as e:
        print(f"Error in generate-code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

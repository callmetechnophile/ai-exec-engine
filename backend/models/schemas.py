from pydantic import BaseModel
from typing import List, Optional

class ProjectQuery(BaseModel):
    query: str

class ProjectInfo(BaseModel):
    project_name: str
    domain: str
    difficulty: str

class ProjectResult(BaseModel):
    title: str
    summary: str
    source: str
    url: str
    thumbnail: Optional[str] = None

class Component(BaseModel):
    name: str
    description: str
    estimated_price: float

class AnalysisResponse(BaseModel):
    project_info: ProjectInfo
    projects: List[ProjectResult]
    electronics: List[Component]
    structural: List[Component]
    mechanical: List[Component]
    pneumatic: List[Component]
    fluid_power: List[Component]

class SpeechResponse(BaseModel):
    text: str

class ExecutionRequest(BaseModel):
    query: str
    components: List[dict]
    budget: int
    complexity: str
    time: str

class ExecutionPackageResponse(BaseModel):
    execution_score: int
    optimized_components: List[dict]
    engineering_recommendations: List[str]
    research_insights: List[str]
    alternative_components: List[dict]
    gantt_tasks: List[dict]
    critical_path: List[str]
    generated_visualization: str
    pdf_export_path: str
    csv_export_path: str
    markdown_export_path: str

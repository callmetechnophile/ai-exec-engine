from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load the environment variables from keys.env before importing any modules
load_dotenv(os.path.join(os.path.dirname(__file__), "keys.env"))

from routes import analyze, speech, research, agentic, export, orchestrator, workspace, chat_recommendation

app = FastAPI(
    title="Engineering Research Assistant API",
    description="Autonomous multi-agent engineering execution platform.",
    version="5.0.0"
)

# Allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(speech.router, prefix="/api", tags=["speech"])
app.include_router(research.router, prefix="/api", tags=["research"])
app.include_router(agentic.router, prefix="/api", tags=["agentic"])
app.include_router(export.router, prefix="/api", tags=["export"])
app.include_router(orchestrator.router, prefix="/api", tags=["orchestrator"])
app.include_router(workspace.router, prefix="/api", tags=["workspace"])
app.include_router(chat_recommendation.router, prefix="/api", tags=["chat_recommendation"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

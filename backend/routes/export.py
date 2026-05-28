from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")

@router.get("/export/{export_type}/{filename}")
async def download_export(export_type: str, filename: str):
    valid_types = ["pdf", "markdown", "csv", "json"]
    if export_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid export type")
        
    file_path = os.path.abspath(os.path.join(EXPORT_DIR, export_type, filename))
    # Prevent directory traversal
    if not file_path.startswith(os.path.abspath(EXPORT_DIR)):
        raise HTTPException(status_code=403, detail="Forbidden")
        
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Export file not found")
        
    return FileResponse(path=file_path, filename=filename)

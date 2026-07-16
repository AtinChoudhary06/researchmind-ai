"""
FastAPI backend for ResearchMind AI.
Run with: uvicorn backend.main:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.agents.planner import run_pipeline
from backend.agents.report_agent import export_to_pdf

app = FastAPI(title="ResearchMind AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this before deploying publicly
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str
    max_papers: int = 4


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(req: ResearchRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="topic cannot be empty")

    result = run_pipeline(req.topic, max_papers=req.max_papers)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.post("/research/report")
def research_report(req: ResearchRequest):
    result = run_pipeline(req.topic, max_papers=req.max_papers)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    pdf_path = export_to_pdf(result)
    return FileResponse(pdf_path, media_type="application/pdf", filename="research_report.pdf")

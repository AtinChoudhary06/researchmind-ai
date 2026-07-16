"""
Planner Agent — the brain.
Given one research topic, it decides and runs the full task sequence:
search -> download -> extract -> summarize -> compare -> find gaps -> write review.

The user never calls individual agents. They call `run_pipeline(topic)` once.
"""
import time

from backend.agents.search_agent import search_papers
from backend.agents.pdf_agent import fetch_and_extract
from backend.agents.summary_agent import summarize_all
from backend.agents.comparison_agent import build_comparison_table
from backend.agents.gap_agent import find_research_gaps
from backend.agents.report_writer_agent import generate_literature_review


def run_pipeline(topic: str, max_papers: int = 4, progress_callback=None) -> dict:
    """
    progress_callback(step_name: str) is optional — pass a function (e.g. a
    Streamlit status updater) to get live progress in the UI.
    """
    def report(step):
        if progress_callback:
            progress_callback(step)

    t0 = time.time()

    report("🔍 Searching ArXiv...")
    papers = search_papers(topic, max_results=max_papers)
    if not papers:
        return {"topic": topic, "error": "No papers found for this query."}

    report(f"📥 Downloading & reading {len(papers)} PDFs...")
    papers = [fetch_and_extract(p) for p in papers]

    report("🧠 Summarizing each paper...")
    papers = summarize_all(papers)

    report("📊 Building comparison table...")
    comparison_table = build_comparison_table(papers)

    report("🕳️ Finding research gaps...")
    gaps = find_research_gaps(topic, papers)

    report("📝 Writing literature review...")
    literature_review = generate_literature_review(topic, papers, gaps)

    report("✅ Done.")

    return {
        "topic": topic,
        "papers": papers,
        "comparison_table": comparison_table,
        "research_gaps": gaps,
        "literature_review": literature_review,
        "elapsed_seconds": round(time.time() - t0, 1),
    }

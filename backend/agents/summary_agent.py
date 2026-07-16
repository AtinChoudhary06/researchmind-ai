"""
Summarizer Agent
Turns raw paper text into a structured summary (title, methodology, dataset,
results, limitations, etc.) using one JSON-mode LLM call per paper.
"""
from backend.utils.llm import call_llm_json

SYSTEM_PROMPT = """You are a research paper analyst. Given the extracted text of an
academic paper, return ONLY a JSON object with these exact keys:

{
  "main_idea": "1-2 sentence summary of the core contribution",
  "methodology": "short description of the method/approach used",
  "dataset": "dataset(s) used, or 'not specified'",
  "results": "key quantitative results if present, else key qualitative findings",
  "advantages": ["short bullet", "short bullet"],
  "limitations": ["short bullet", "short bullet"]
}

Be concise. Do not include any text outside the JSON object."""


def summarize_paper(paper: dict) -> dict:
    user_prompt = f"""Title: {paper['title']}
Abstract: {paper['abstract']}

Extracted paper text (may be partial):
{paper['full_text']}"""

    summary = call_llm_json(SYSTEM_PROMPT, user_prompt)
    paper["summary"] = summary
    return paper


def summarize_all(papers: list[dict]) -> list[dict]:
    return [summarize_paper(p) for p in papers]

"""
Research Gap Agent
Looks across ALL paper summaries together (not one at a time) and identifies
patterns, blind spots, and unexplored directions. This is the "wow" feature
in interviews — it requires reasoning over the full set, not just per-paper.
"""
from backend.utils.llm import call_llm

SYSTEM_PROMPT = """You are a senior research scientist writing the "Research Gaps"
section of a literature survey. You will be given structured summaries of several
papers on the same topic. Identify:

1. Patterns common across most papers (methods, datasets, assumptions everyone shares)
2. What is NOT being addressed (research gaps)
3. Concrete, specific future research directions

Write 4-6 crisp bullet points. Be specific to what you were given — do not write
generic filler like "more research is needed"."""


def find_research_gaps(topic: str, papers: list[dict]) -> str:
    summaries_text = "\n\n".join(
        f"Paper {i+1}: {p['title']}\n"
        f"Main idea: {p.get('summary', {}).get('main_idea', 'N/A')}\n"
        f"Methodology: {p.get('summary', {}).get('methodology', 'N/A')}\n"
        f"Dataset: {p.get('summary', {}).get('dataset', 'N/A')}\n"
        f"Limitations: {p.get('summary', {}).get('limitations', [])}"
        for i, p in enumerate(papers)
    )

    user_prompt = f"Research topic: {topic}\n\nPaper summaries:\n{summaries_text}"
    return call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.4)

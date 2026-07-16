"""
Literature Review Agent
Writes a survey-style literature review from the summarized papers + research gaps.
"""
from backend.utils.llm import call_llm

SYSTEM_PROMPT = """You are writing the "Literature Review" section of an academic
survey paper. Given a topic, paper summaries, and identified research gaps, write
a well-structured literature review with these sections:

## Introduction
## Background
## Summary of Existing Work
## Comparative Analysis
## Research Gaps
## Future Work

Reference papers by their titles inline (not numbered citations). Keep it factual
and grounded only in the summaries provided — do not invent findings. Aim for
roughly 400-600 words total."""


def generate_literature_review(topic: str, papers: list[dict], gaps_text: str) -> str:
    summaries_text = "\n\n".join(
        f"- {p['title']}: {p.get('summary', {}).get('main_idea', 'N/A')} "
        f"(Method: {p.get('summary', {}).get('methodology', 'N/A')}, "
        f"Results: {p.get('summary', {}).get('results', 'N/A')})"
        for p in papers
    )

    user_prompt = f"""Topic: {topic}

Paper summaries:
{summaries_text}

Research gaps already identified:
{gaps_text}"""

    return call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.4)

"""
Comparison Agent (Phase 2)
Builds a simple comparison table across already-summarized papers.
No LLM call needed here — it's pure formatting off structured summaries.
"""


def build_comparison_table(papers: list[dict]) -> list[dict]:
    rows = []
    for p in papers:
        s = p.get("summary", {})
        rows.append({
            "Paper": p["title"][:60] + ("..." if len(p["title"]) > 60 else ""),
            "Methodology": s.get("methodology", "-"),
            "Dataset": s.get("dataset", "-"),
            "Results": s.get("results", "-"),
            "Limitations": "; ".join(s.get("limitations", [])) or "-",
        })
    return rows

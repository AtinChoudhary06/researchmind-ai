"""
Search Agent
Today this calls the `arxiv` python package directly.
Later, swap the body of `search_papers` to call your ArXiv MCP server instead —
the return shape (list[dict]) stays identical, so nothing downstream changes.
"""
import arxiv


def search_papers(query: str, max_results: int = 4) -> list[dict]:
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in client.results(search):
        papers.append({
            "id": result.entry_id.split("/")[-1],
            "title": result.title.strip(),
            "authors": [a.name for a in result.authors],
            "published": str(result.published.date()) if result.published else None,
            "abstract": result.summary.strip().replace("\n", " "),
            "pdf_url": result.pdf_url,
            "primary_category": result.primary_category,
        })
    return papers

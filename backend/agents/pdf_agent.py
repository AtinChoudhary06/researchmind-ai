"""
PDF Reader Agent
Downloads each paper's PDF and extracts raw text.
Later, swap `download_pdf` to write via the Filesystem MCP server so every
agent in the pipeline shares one real filesystem instead of a local folder.
"""
import os
import requests
import pdfplumber

PAPERS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "papers")
os.makedirs(PAPERS_DIR, exist_ok=True)

MAX_CHARS_FOR_LLM = 12000  # keep prompt sizes sane; enough for abstract+methods+results


def download_pdf(paper_id: str, pdf_url: str) -> str:
    path = os.path.join(PAPERS_DIR, f"{paper_id}.pdf")
    if os.path.exists(path):
        return path

    resp = requests.get(pdf_url, timeout=30)
    resp.raise_for_status()
    with open(path, "wb") as f:
        f.write(resp.content)
    return path


def extract_text(pdf_path: str) -> str:
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    full_text = "\n".join(text_parts)
    return full_text[:MAX_CHARS_FOR_LLM]


def fetch_and_extract(paper: dict) -> dict:
    """Downloads + extracts text for one paper dict from search_agent. Adds 'full_text' key."""
    try:
        pdf_path = download_pdf(paper["id"], paper["pdf_url"])
        text = extract_text(pdf_path)
        paper["full_text"] = text if text.strip() else paper["abstract"]
        paper["pdf_local_path"] = pdf_path
    except Exception as e:
        # fall back to abstract only — keeps the pipeline alive if one PDF fails
        paper["full_text"] = paper["abstract"]
        paper["pdf_local_path"] = None
        paper["extraction_error"] = str(e)
    return paper

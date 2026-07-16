"""
Report Agent
Exports the pipeline result (literature review + comparison table + gaps)
to a PDF file the user can download.
"""
import os
from fpdf import FPDF

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


class _ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "ResearchMind AI - Literature Review Report", ln=True, align="C")
        self.ln(2)


def _write_wrapped(pdf: FPDF, text: str, size: int = 11, style: str = ""):
    pdf.set_font("Helvetica", style, size)
    safe_text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 6, safe_text)
    pdf.ln(1)


def export_to_pdf(result: dict) -> str:
    pdf = _ReportPDF()
    pdf.add_page()

    _write_wrapped(pdf, f"Topic: {result['topic']}", size=13, style="B")
    pdf.ln(2)

    _write_wrapped(pdf, "Literature Review", size=12, style="B")
    _write_wrapped(pdf, result.get("literature_review", ""))

    _write_wrapped(pdf, "Research Gaps", size=12, style="B")
    _write_wrapped(pdf, result.get("research_gaps", ""))

    _write_wrapped(pdf, "Paper Comparison", size=12, style="B")
    for row in result.get("comparison_table", []):
        line = " | ".join(f"{k}: {v}" for k, v in row.items())
        _write_wrapped(pdf, line, size=9)

    _write_wrapped(pdf, "Papers Reviewed", size=12, style="B")
    for p in result.get("papers", []):
        _write_wrapped(pdf, f"- {p['title']} ({', '.join(p['authors'][:3])})", size=10)

    safe_topic = "".join(c if c.isalnum() else "_" for c in result["topic"])[:40]
    out_path = os.path.join(REPORTS_DIR, f"{safe_topic}_report.pdf")
    pdf.output(out_path)
    return out_path

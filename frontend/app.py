"""
Streamlit UI for ResearchMind AI.
Run with: streamlit run frontend/app.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend.agents.planner import run_pipeline
from backend.agents.report_agent import export_to_pdf

st.set_page_config(page_title="ResearchMind AI", page_icon="🧠", layout="wide")

st.title("🧠 ResearchMind AI — Multi-Agent Research Copilot")
st.caption("Type a topic. The planner agent searches ArXiv, reads papers, compares them, "
           "finds research gaps, and writes a literature review — no manual steps.")

with st.form("research_form"):
    topic = st.text_input("Research topic", placeholder="e.g. RAG evaluation techniques")
    max_papers = st.slider("Number of papers", min_value=2, max_value=6, value=4)
    submitted = st.form_submit_button("Run ResearchMind 🚀")

if submitted and topic.strip():
    status_box = st.status("Planning...", expanded=True)

    def update_status(step):
        status_box.write(step)

    result = run_pipeline(topic, max_papers=max_papers, progress_callback=update_status)
    status_box.update(label="Pipeline complete", state="complete")

    if "error" in result:
        st.error(result["error"])
    else:
        st.session_state["last_result"] = result

if "last_result" in st.session_state:
    result = st.session_state["last_result"]

    st.success(f"Done in {result['elapsed_seconds']}s — {len(result['papers'])} papers analyzed.")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📚 Papers", "📊 Comparison", "🕳️ Research Gaps", "📝 Literature Review"]
    )

    with tab1:
        for p in result["papers"]:
            with st.expander(p["title"]):
                st.write(f"**Authors:** {', '.join(p['authors'])}")
                st.write(f"**Published:** {p.get('published', 'N/A')}")
                st.write(f"**Abstract:** {p['abstract']}")
                s = p.get("summary", {})
                st.markdown(f"**Main idea:** {s.get('main_idea', 'N/A')}")
                st.markdown(f"**Methodology:** {s.get('methodology', 'N/A')}")
                st.markdown(f"**Dataset:** {s.get('dataset', 'N/A')}")
                st.markdown(f"**Results:** {s.get('results', 'N/A')}")
                st.markdown("**Advantages:** " + ", ".join(s.get("advantages", [])))
                st.markdown("**Limitations:** " + ", ".join(s.get("limitations", [])))
                st.markdown(f"[Open PDF]({p['pdf_url']})")

    with tab2:
        st.table(result["comparison_table"])

    with tab3:
        st.markdown(result["research_gaps"])

    with tab4:
        st.markdown(result["literature_review"])

    st.divider()
    if st.button("📄 Export full report as PDF"):
        pdf_path = export_to_pdf(result)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="researchmind_report.pdf")

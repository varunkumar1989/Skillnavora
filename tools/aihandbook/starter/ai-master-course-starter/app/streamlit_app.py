"""Streamlit front end for the PDF chatbot.
Run: streamlit run app/streamlit_app.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from starter.config import settings
from starter.rag import answer, index_pdf

SAMPLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_policy.pdf")

st.set_page_config(page_title="PDF chatbot", page_icon="📄")
st.title("Ask your PDF")
st.caption("Offline mode: answers are quoted sentences, no API key needed." if settings.offline
           else f"Using Claude model {settings.model}.")


@st.cache_resource
def sample_store():
    return index_pdf(SAMPLE)


uploaded = st.sidebar.file_uploader("Upload a PDF (or use the sample policy)", type="pdf")
if uploaded:
    key = f"store-{uploaded.name}-{uploaded.size}"
    if key not in st.session_state:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, uploaded.name)
            with open(path, "wb") as f:
                f.write(uploaded.getvalue())
            st.session_state[key] = index_pdf(path)
    store, doc_name = st.session_state[key], uploaded.name
else:
    store, doc_name = sample_store(), "sample_policy.pdf"
st.sidebar.write(f"**Document:** {doc_name}  \n**Chunks:** {len(store.items)}")
k = st.sidebar.slider("Sources to retrieve (k)", 1, 6, 3)

if "history" not in st.session_state:
    st.session_state.history = []
for role, text in st.session_state.history:
    st.chat_message(role).write(text)

question = st.chat_input("Ask a question about the document")
if question:
    st.chat_message("user").write(question)
    try:
        result = answer(store, question, k=k)
    except RuntimeError as e:
        result = {"answer": f"Error: {e}", "sources": []}
    with st.chat_message("assistant"):
        st.write(result["answer"])
        if result.get("sources"):
            with st.expander("Sources and cost"):
                for s in result["sources"]:
                    st.write(f"{s['tag']}: {s['file']}, page {s['page']} (score {s['score']})")
                if result.get("tokens"):
                    st.write(f"Tokens in/out: {result['tokens']['input']}/{result['tokens']['output']}, "
                             f"cost about ${result['cost_usd']:.5f}")
    st.session_state.history += [("user", question), ("assistant", result["answer"])]

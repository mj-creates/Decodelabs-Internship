import streamlit as st
import fitz  # pymupdf
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.set_page_config(page_title="Knowledge Analyst", page_icon="📚", layout="wide")
st.title("📚 AI Knowledge Analyst — RAG Document Intelligence")

def extract_text_with_pages(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        pages.append({
            "page": i + 1,
            "text": page.get_text()
        })
    return pages

def build_context(pages):
    context = ""
    for p in pages:
        context += f"\n\n--- PAGE {p['page']} ---\n{p['text']}"
    return context

def ask_question(context, question):
    prompt = f"""You are a legal document analyst. 
You have been given a document below. Answer the question using ONLY information from the document.
For every fact you state, cite the exact page number like this: [Page X]
If the answer is not in the document, say "This information is not found in the document."

DOCUMENT:
{context[:12000]}

QUESTION: {question}

Answer with citations:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def extract_dashboard(context):
    prompt = f"""You are a legal document analyst. Analyze this document and extract:

1. RISKS: List all potential risks, penalties, or liabilities mentioned (max 5)
2. DATES: List all important dates and deadlines mentioned
3. STAKEHOLDERS: List all parties, companies, or people mentioned

Document:
{context[:12000]}

Respond ONLY in this exact format:
RISKS:
- risk 1
- risk 2

DATES:
- date 1
- date 2

STAKEHOLDERS:
- stakeholder 1
- stakeholder 2"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# UI
uploaded_file = st.file_uploader("Upload a legal/contract PDF", type="pdf")

if uploaded_file:
    with st.spinner("Reading document..."):
        pages = extract_text_with_pages(uploaded_file)
        context = build_context(pages)
        st.success(f"✅ Document loaded — {len(pages)} pages")

    tab1, tab2 = st.tabs(["💬 Ask Questions", "📊 Summary Dashboard"])

    with tab1:
        st.subheader("Ask anything about the document")
        question = st.text_input("Your question:", placeholder="What are the termination conditions?")
        if st.button("Ask") and question:
            with st.spinner("Analyzing..."):
                answer = ask_question(context, question)
            st.markdown("### Answer")
            st.write(answer)

    with tab2:
        st.subheader("Auto-extracted Intelligence")
        if st.button("Generate Dashboard"):
            with st.spinner("Extracting key information..."):
                dashboard = extract_dashboard(context)
            
            sections = dashboard.split("\n\n")
            col1, col2, col3 = st.columns(3)
            
            for section in sections:
                if section.startswith("RISKS:"):
                    with col1:
                        st.markdown("### 🚨 Risks")
                        items = [l.strip("- ") for l in section.split("\n")[1:] if l.strip()]
                        for item in items:
                            if item:
                                st.error(item)
                elif section.startswith("DATES:"):
                    with col2:
                        st.markdown("### 📅 Dates")
                        items = [l.strip("- ") for l in section.split("\n")[1:] if l.strip()]
                        for item in items:
                            if item:
                                st.info(item)
                elif section.startswith("STAKEHOLDERS:"):
                    with col3:
                        st.markdown("### 👥 Stakeholders")
                        items = [l.strip("- ") for l in section.split("\n")[1:] if l.strip()]
                        for item in items:
                            if item:
                                st.success(item)
import os
import streamlit as st
import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv

# Securely load the .env file if it exists locally
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Contract Clarity Copilot",
    page_icon="⚖️",
    layout="wide"
)

# --- DISCLAIMER ---
st.warning(
    "⚠️ **Disclaimer:** This tool uses Generative AI to assist in understanding legal text. "
    "It provides educational summaries and information, **NOT professional legal advice**. "
    "Always consult a licensed attorney for binding legal counsel."
)

# --- SIDEBAR: CONFIGURATION & UPLOAD ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for the key in the .env file first
    default_key = os.environ.get("GEMINI_API_KEY", "")
    
    # type="password" ensures the key shows as dots (••••••) during your video recording
    api_key = st.text_input(
        "Gemini API Key", 
        value=default_key, 
        type="password",
        help="Paste your Google AI Studio API key here."
    )
    
    st.divider()
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload an Agreement or Contract (PDF)", type=["pdf"])

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for index, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {index + 1} ---\n" + page_text
        return text
    except Exception as exc:
        st.error(f"Error reading PDF: {exc}")
        return ""

def generate_legal_response(prompt, context, user_key):
    genai.configure(api_key=user_key)
    
    system_instruction = (
        "You are an objective AI document analyst assisting users in understanding legal documents.\n"
        "STRICT OPERATING RULES:\n"
        "1. Base answers exclusively on the provided text. Do not invent terms or assumptions.\n"
        "2. If the user asks whether they should sign, or requests legal advice, decline and "
        "instruct them to consult a qualified attorney.\n"
        "3. Explain complex clauses clearly at an accessible 8th-grade reading level.\n"
        "4. Highlight risks, ambiguities, deadlines, and financial obligations clearly."
    )
    
    full_prompt = f"{system_instruction}\n\nDOCUMENT CONTEXT:\n{context}\n\nUSER REQUEST:\n{prompt}"
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as exc:
        return f"AI Generation Error: {exc}"

# --- MAIN WORKSPACE ---
st.title("⚖️ Contract Clarity Copilot")
st.write("Understand terms, clarify ambiguities, and prepare for legal consultations.")

if not api_key:
    st.info("👈 Enter your Gemini API Key in the sidebar to get started.")
elif uploaded_file is None:
    st.info("👈 Upload a PDF contract in the sidebar to begin analysis.")
else:
    if "doc_text" not in st.session_state or st.session_state.get("current_file") != uploaded_file.name:
        with st.spinner("Extracting and parsing document..."):
            st.session_state.doc_text = extract_text_from_pdf(uploaded_file)
            st.session_state.current_file = uploaded_file.name
        st.success(f"Loaded: {uploaded_file.name}")

    document_text = st.session_state.doc_text

    tab_qa, tab_jargon, tab_checklist = st.tabs([
        "💬 Document Q&A", 
        "🔍 Clause Simplifier", 
        "📋 Lawyer Prep Checklist"
    ])

    with tab_qa:
        st.subheader("Ask Questions About This Contract")
        user_query = st.text_input("Enter your question:", placeholder="e.g., What are the terms of termination?")
        if st.button("Submit Question", key="btn_qa"):
            if user_query.strip():
                with st.spinner("Searching document terms..."):
                    answer = generate_legal_response(
                        f"Answer the following query using the document text: {user_query}",
                        document_text,
                        api_key
                    )
                    st.markdown("### Answer")
                    st.markdown(answer)
            else:
                st.warning("Please type a question before submitting.")

    with tab_jargon:
        st.subheader("Simplify Dense Legal Jargon")
        clause_input = st.text_area(
            "Paste clause here:",
            height=130,
            placeholder="e.g., 'Indemnification: The counterparty agrees to hold harmless...'"
        )
        if st.button("Translate Clause", key="btn_jargon"):
            if clause_input.strip():
                with st.spinner("Simplifying legal phrasing..."):
                    simplified = generate_legal_response(
                        f"Translate this legal clause into plain, easy-to-understand language.\n\n{clause_input}",
                        document_text,
                        api_key
                    )
                    st.markdown("### Plain-English Breakdown")
                    st.markdown(simplified)
            else:
                st.warning("Please paste a clause to analyze.")

    with tab_checklist:
        st.subheader("Generate Consultation Questions")
        if st.button("Generate Checklist", key="btn_checklist"):
            with st.spinner("Scanning for risk flags and ambiguities..."):
                checklist_prompt = (
                    "Scan this agreement and generate an actionable bulleted checklist of 4-6 specific "
                    "questions or issues the user should raise with their lawyer before signing."
                )
                checklist_output = generate_legal_response(checklist_prompt, document_text, api_key)
                st.markdown("### Attorney Consultation Checklist")
                st.markdown(checklist_output)

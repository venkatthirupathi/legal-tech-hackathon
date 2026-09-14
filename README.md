# ⚖️ Contract Clarity Copilot

**Contract Clarity Copilot** is a GenAI-powered web application built for the Legal Tech Hackathon. It makes legal documents accessible by translating complex jargon into plain English, answering specific questions based on the text, and generating actionable prep checklists for legal consultations.

## 🚀 Key Features
* **Document Parsing:** Securely extracts text from uploaded PDF contracts.
* **Live Q&A:** Ask specific questions about obligations and dates within the document.
* **Jargon Translator:** Simplifies complex legal clauses into an 8th-grade reading level.
* **Lawyer Prep Checklist:** Generates a list of critical questions to ask an actual attorney.
* **Strict Guardrails:** The AI is explicitly prompted to refuse giving direct legal advice.

## 💻 How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add: `GEMINI_API_KEY=your_key_here`
4. Run the app: `streamlit run app.py`

> **Disclaimer:** This tool is for informational purposes only and does not constitute professional legal advice.

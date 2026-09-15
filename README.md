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
3. Copy `.env.example` to `.env` and set your key: `GEMINI_API_KEY=your_key_here`
4. Run the app: `streamlit run app.py`

## ☁️ Deploy on Streamlit Community Cloud
1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from this repo and set `app.py` as the entrypoint.
3. In **App settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY="your_key_here"
   ```
4. Deploy the app.

## ☁️ Deploy on Google Cloud Run
1. Build and push the container:
   - `gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/legal-tech-hackathon`
2. Deploy to Cloud Run:
   - `gcloud run deploy legal-tech-hackathon --image gcr.io/YOUR_PROJECT_ID/legal-tech-hackathon --platform managed --region YOUR_REGION --allow-unauthenticated --set-env-vars GEMINI_API_KEY=your_key_here`
3. Open the Cloud Run URL after deployment completes.

## ✅ Deployment Readiness Checklist
- Dependencies install from `requirements.txt`
- App starts with `streamlit run app.py`
- Docker image builds successfully from `Dockerfile`
- `GEMINI_API_KEY` is provided through environment/secrets (never committed)

> **Disclaimer:** This tool is for informational purposes only and does not constitute professional legal advice.

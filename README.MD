# Autonomous Finance Analyst 📊

A specialized Retrieval-Augmented Generation (RAG) pipeline built to dynamically calculate unit economics (CAC & LTV) from internal company data.

## System Architecture
* **Frontend:** Streamlit (Manual Session State Management)
* **LLM Engine:** Groq API (`llama3-8b-8192`)
* **Retrieval:** Custom Keyword/Sparse Search Engine with Context Injection

## Production Failure Modes Mitigated
Building this system required solving several real-world LLMOps challenges:
1. **Amnesia & UI Wipes:** Mitigated Streamlit's top-to-bottom execution rerun by implementing robust `st.session_state` dictionary appending for conversational memory.
2. **Context Bleed:** Engineered an invisible Context Injection step. The application retrieves and appends internal financial data to the LLM's prompt payload without displaying the raw database strings in the user-facing chat UI.
3. **Model Deprecation Handling:** Navigated `400 model_decommissioned` cloud infrastructure failures by writing custom diagnostic scripts to query the Groq API for active endpoints and dynamically update routing logic.
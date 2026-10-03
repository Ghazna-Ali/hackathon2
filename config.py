"""Configuration + LLM factory. Keys come from Streamlit secrets or env vars."""
import os


def get_secret(name: str, default=None):
    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name, default)


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def get_llm(temperature: float = 0.2, api_key: str | None = None):
    """Gemini by default (per the hackathon guide). Set LLM_PROVIDER=groq to switch."""
    provider = str(get_secret("LLM_PROVIDER", "gemini")).lower()

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=get_secret("GROQ_MODEL", "llama-3.3-70b-versatile"),
            temperature=temperature,
            api_key=api_key or get_secret("GROQ_API_KEY"),
        )

    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model=get_secret("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=temperature,
        google_api_key=api_key or get_secret("GOOGLE_API_KEY"),
    )

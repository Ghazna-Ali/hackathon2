"""RAG layer: read documents, chunk, embed, store in Chroma, retrieve by source."""
import io
import uuid

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from config import CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL


def load_uploaded_file(uploaded_file, source_type: str) -> list[Document]:
    """Turn a Streamlit UploadedFile (PDF or TXT) into per-page Documents."""
    data = uploaded_file.getvalue()
    name = uploaded_file.name
    docs = []
    if name.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        for i, page in enumerate(reader.pages):
            text = (page.extract_text() or "").strip()
            if text:
                docs.append(Document(
                    page_content=text,
                    metadata={"source_type": source_type, "file": name, "page": i + 1},
                ))
    else:
        text = data.decode("utf-8", errors="ignore").strip()
        if text:
            docs.append(Document(
                page_content=text,
                metadata={"source_type": source_type, "file": name, "page": 1},
            ))
    return docs


def text_to_documents(text: str, source_type: str, name: str = "pasted_text") -> list[Document]:
    text = (text or "").strip()
    if not text:
        return []
    return [Document(page_content=text,
                     metadata={"source_type": source_type, "file": name, "page": 1})]


def get_embeddings():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def build_vectorstore(documents: list[Document], embeddings):
    from langchain_chroma import Chroma
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        # unique name so different sessions/runs never share data
        collection_name=f"career_{uuid.uuid4().hex[:10]}",
    )


def retrieve(vectorstore, query: str, source_type: str, k: int = 6):
    """Return (context_text, evidence_list) limited to CV or JOB_DESCRIPTION chunks."""
    docs = vectorstore.similarity_search(query, k=k, filter={"source_type": source_type})
    context = "\n\n".join(d.page_content for d in docs)
    evidence = [{
        "source": d.metadata.get("source_type"),
        "file": d.metadata.get("file"),
        "page": d.metadata.get("page"),
        "text": d.page_content,
    } for d in docs]
    return context, evidence

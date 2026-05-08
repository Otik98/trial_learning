import os
import re
import fitz
import faiss
import numpy as np

from groq import Groq
from sentence_transformers import SentenceTransformer, CrossEncoder
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_FOLDER = "rag_articles"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"


def clean_text(text):
    """Clean extracted PDF text."""
    text = re.sub(r"\b(\w+)(\s+\1){2,}\b", r"\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_and_parse_documents():
    """Load PDF files from rag_articles folder and extract text."""
    documents = []

    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(f"Folder '{DATA_FOLDER}' was not found.")

    for filename in os.listdir(DATA_FOLDER):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(DATA_FOLDER, filename)

            doc = fitz.open(filepath)
            full_text = ""

            for page in doc:
                full_text += page.get_text()

            full_text = clean_text(full_text)

            if full_text:
                documents.append({
                    "name": filename,
                    "text": full_text
                })

    if not documents:
        raise ValueError("No PDF documents were found in rag_articles folder.")

    return documents


def load_models_and_build_index():
    """
    Build RAG pipeline:
    PDF documents -> chunks -> embeddings -> FAISS index.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set.")

    groq_client = Groq(api_key=GROQ_API_KEY)

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    cross_encoder_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    documents = load_and_parse_documents()

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    parent_docs_store = {}
    child_to_parent_map = {}
    child_chunks_for_embedding = []

    doc_id_counter = 0

    for doc in documents:
        parent_chunks = parent_splitter.split_text(doc["text"])

        for chunk_id_counter, parent_chunk_text in enumerate(parent_chunks):
            parent_id = f"{doc_id_counter}_{chunk_id_counter}"

            parent_docs_store[parent_id] = {
                "text": parent_chunk_text,
                "source": doc["name"]
            }

            child_chunks = child_splitter.split_text(parent_chunk_text)

            for child_chunk_text in child_chunks:
                child_chunks_for_embedding.append(child_chunk_text)
                child_to_parent_map[len(child_chunks_for_embedding) - 1] = parent_id

        doc_id_counter += 1

    embeddings = embedding_model.encode(
        child_chunks_for_embedding,
        show_progress_bar=True
    )

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return {
        "groq_client": groq_client,
        "embedding_model": embedding_model,
        "cross_encoder": cross_encoder_model,
        "index": index,
        "child_chunks": child_chunks_for_embedding,
        "child_to_parent_map": child_to_parent_map,
        "parent_store": parent_docs_store,
    }


def retrieve_and_rerank(query, rag_components, k_retriever=30, k_reranker=5):
    """Retrieve relevant chunks using FAISS and rerank them with CrossEncoder."""
    embedding_model = rag_components["embedding_model"]
    cross_encoder = rag_components["cross_encoder"]
    index = rag_components["index"]

    total_vectors = index.ntotal
    k_retriever = min(k_retriever, total_vectors)

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    _, indices = index.search(query_embedding, k_retriever)

    unique_indices = np.unique(indices.flatten())
    unique_indices = [i for i in unique_indices if i >= 0]

    retrieved_child_chunks = [
        rag_components["child_chunks"][i] for i in unique_indices
    ]

    pairs = [(query, chunk) for chunk in retrieved_child_chunks]
    scores = cross_encoder.predict(pairs, show_progress_bar=False)

    reranked_indices = np.argsort(scores)[::-1]

    final_context_chunks = []
    seen_parent_ids = set()

    for i in reranked_indices[:k_reranker]:
        original_child_index = unique_indices[i]
        parent_id = rag_components["child_to_parent_map"][original_child_index]

        if parent_id not in seen_parent_ids:
            final_context_chunks.append(rag_components["parent_store"][parent_id])
            seen_parent_ids.add(parent_id)

    return final_context_chunks


def generate_answer(query, context, groq_client=None):
    """Generate answer using Groq LLM based only on retrieved context."""
    context_str = "\n\n---\n\n".join(
        [
            f"Source: {chunk['source']}\nText: {chunk['text'][:1200]}"
            for chunk in context
        ]
    )

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful research assistant. "
                    "Answer only using the provided context. "
                    "If the answer is not found in the context, say: "
                    "'The provided documents do not contain enough information to answer this question.' "
                    "Answer in English. Be clear and concise."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context_str}\n\nQuestion: {query}"
            }
        ],
        max_tokens=512,
        temperature=0.3,
    )

    return response.choices[0].message.content

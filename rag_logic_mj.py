import os
import re
import pandas as pd
import numpy as np
import faiss
from groq import Groq
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_FILE = "data/mj_articles.csv"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"


def clean_text(text):
    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_documents():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError("Cannot find data/mj_articles.csv")

    df = pd.read_csv(DATA_FILE)

    required_columns = {"title", "url", "text"}
    if not required_columns.issubset(df.columns):
        raise ValueError("mj_articles.csv must contain: title, url, text")

    docs = []

    for _, row in df.iterrows():
        text = clean_text(row["text"])

        if len(text) > 20:
            docs.append({
                "source": str(row["title"]),
                "url": str(row["url"]),
                "text": text
            })

    if not docs:
        raise ValueError("No useful text found in mj_articles.csv")

    return docs


def load_models_and_build_index():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Add it in Streamlit Cloud Secrets.")

    groq_client = Groq(api_key=GROQ_API_KEY)

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = []

    for doc in documents:
        parts = splitter.split_text(doc["text"])

        for part in parts:
            chunks.append({
                "text": part,
                "source": doc["source"],
                "url": doc["url"]
            })

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return {
        "groq_client": groq_client,
        "embedding_model": embedding_model,
        "index": index,
        "chunks": chunks
    }


def retrieve_and_rerank(query, rag_components, k_retriever=4):
    embedding_model = rag_components["embedding_model"]
    index = rag_components["index"]
    chunks = rag_components["chunks"]

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    k = min(k_retriever, len(chunks))
    _, indices = index.search(query_embedding, k)

    results = []

    for i in indices.flatten():
        if i != -1:
            results.append(chunks[i])

    return results


def generate_answer(query, context, groq_client=None):
    if not context:
        return "I could not find an answer in the provided Michael Jackson sources."

    context_text = "\n\n---\n\n".join(
        [
            f"Source: {chunk['source']}\nURL: {chunk['url']}\nText: {chunk['text']}"
            for chunk in context
        ]
    )

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful RAG assistant for a Michael Jackson project. "
                    "Answer only using the provided context. "
                    "If the answer is not in the context, say that the provided sources do not contain the answer. "
                    "Answer in the same language as the user. "
                    "Be clear and concise."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {query}"
            }
        ],
        max_tokens=500,
        temperature=0.3
    )

    return response.choices[0].message.content

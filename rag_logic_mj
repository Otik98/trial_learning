import os
import re
import requests
import fitz  # PyMuPDF
from groq import Groq
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Конфигурация ---
DATA_FOLDER = "rag_articles"
ARTICLES = [
    {
        "filename": "s40684_020_00302_7.pdf",
        "url": "https://link.springer.com/content/pdf/10.1007/s40684-020-00302-7.pdf"
    },
    {
        "filename": "s00170_021_08596_w.pdf",
        "url": "https://link.springer.com/content/pdf/10.1007/s00170-021-08596-w.pdf"
    },
    {
        "filename": "s00170_015_7576_2.pdf",
        "url": "https://link.springer.com/content/pdf/10.1007/s00170-015-7576-2.pdf"
    },
    {
        "filename": "s11665_014_0958_z.pdf",
        "url": "https://link.springer.com/content/pdf/10.1007/s11665-014-0958-z.pdf"
    }
]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL   = "llama-3.1-8b-instant"


# --- Очистка текста ---
def clean_text(text):
    """Убирает повторяющиеся слова и мусор из PDF."""
    # Убираем слово повторяющееся 3+ раз подряд
    text = re.sub(r'\b(\w+)(\s+\1){2,}\b', r'\1', text, flags=re.IGNORECASE)
    # Убираем лишние пробелы и переносы строк
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# --- Загрузка данных ---
def download_articles():
    """Скачивает статьи если ещё не загружены."""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    for article in ARTICLES:
        filepath = os.path.join(DATA_FOLDER, article["filename"])
        if not os.path.exists(filepath):
            print(f"Загрузка: {article['filename']}...")
            try:
                response = requests.get(article["url"])
                response.raise_for_status()
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Загружено: {article['filename']}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке {article['url']}: {e}")


def load_and_parse_documents():
    """Загружает PDF и извлекает очищенный текст."""
    docs = []
    print("Обработка документов...")
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DATA_FOLDER, filename)
            try:
                doc = fitz.open(filepath)
                full_text = "".join(page.get_text() for page in doc)
                full_text = clean_text(full_text)  # очистка от мусора
                docs.append({"name": filename, "text": full_text})
                print(f"Обработан: {filename} ({len(full_text)} символов)")
            except Exception as e:
                print(f"Ошибка {filename}: {e}")
    return docs


# --- Основные функции RAG ---
def load_models_and_build_index():
    """
    Загружает модели и строит FAISS-индекс.
    LLM не загружается локально — используется Groq API.
    """
    print("Инициализируем Groq клиент...")
    groq_client = Groq(api_key=GROQ_API_KEY)

    print("Загружаем embedding модель...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Загружаем Cross-Encoder...")
    cross_encoder_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    download_articles()
    documents = load_and_parse_documents()

    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    child_splitter  = RecursiveCharacterTextSplitter(chunk_size=400,  chunk_overlap=50)

    parent_docs_store          = {}
    child_to_parent_map        = {}
    child_chunks_for_embedding = []

    doc_id_counter = 0
    for doc in documents:
        current_parent_chunks = parent_splitter.split_text(doc['text'])
        chunk_id_counter = 0
        for parent_chunk_text in current_parent_chunks:
            parent_id = f"{doc_id_counter}_{chunk_id_counter}"
            parent_docs_store[parent_id] = {
                "text":   parent_chunk_text,
                "source": doc['name']
            }
            for child_chunk_text in child_splitter.split_text(parent_chunk_text):
                child_chunks_for_embedding.append(child_chunk_text)
                child_to_parent_map[len(child_chunks_for_embedding) - 1] = parent_id
            chunk_id_counter += 1
        doc_id_counter += 1

    print("Создаём эмбеддинги...")
    embeddings = embedding_model.encode(child_chunks_for_embedding, show_progress_bar=True)
    dimension  = embeddings.shape[1]
    index      = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"FAISS индекс: {dimension}d, {index.ntotal} векторов")

    return {
        "groq_client":         groq_client,
        "embedding_model":     embedding_model,
        "cross_encoder":       cross_encoder_model,
        "index":               index,
        "child_chunks":        child_chunks_for_embedding,
        "child_to_parent_map": child_to_parent_map,
        "parent_store":        parent_docs_store,
        # для совместимости
        "llm_model":           None,
        "tokenizer":           None,
    }


def retrieve_and_rerank(query, rag_components, k_retriever=30, k_reranker=5):
    """Векторный поиск + переранжирование через Cross-Encoder."""
    embedding_model = rag_components["embedding_model"]
    cross_encoder   = rag_components["cross_encoder"]
    index           = rag_components["index"]

    # Шаг 1: векторный поиск
    query_embedding = embedding_model.encode([query])
    _, I            = index.search(query_embedding, k_retriever)
    unique_indices  = np.unique(I.flatten())

    # Шаг 2: переранжирование
    retrieved_child_chunks = [rag_components["child_chunks"][i] for i in unique_indices]
    pairs            = [(query, chunk) for chunk in retrieved_child_chunks]
    scores           = cross_encoder.predict(pairs, show_progress_bar=False)
    reranked_indices = np.argsort(scores)[::-1]

    # Шаг 3: уникальные родительские чанки
    final_context_chunks = []
    seen_parent_ids      = set()
    for i in reranked_indices[:k_reranker]:
        original_child_index = unique_indices[i]
        parent_id = rag_components["child_to_parent_map"][original_child_index]
        if parent_id not in seen_parent_ids:
            final_context_chunks.append(rag_components["parent_store"][parent_id])
            seen_parent_ids.add(parent_id)

    return final_context_chunks


def generate_answer(query, context, llm_model=None, tokenizer=None, groq_client=None):
    """Генерирует ответ через Groq API."""
    # Ограничиваем размер каждого чанка чтобы не переполнить контекст
    context_str = "\n\n---\n\n".join([chunk['text'][:500] for chunk in context])

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты — внимательный и точный ассистент-исследователь. "
                    "Отвечай ИСКЛЮЧИТЕЛЬНО на основе предоставленного контекста. "
                    "Если ответ в контексте не найден — скажи: "
                    "'В предоставленном контексте нет ответа на этот вопрос'. "
                    "Отвечай на русском языке. Будь конкретным и кратким."
                )
            },
            {
                "role": "user",
                "content": f"Контекст:\n{context_str}\n\nВопрос: {query}"
            }
        ],
        max_tokens=512,
        temperature=0.7,
    )

    return response.choices[0].message.content

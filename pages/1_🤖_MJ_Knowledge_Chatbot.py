import streamlit as st

from rag_logic_pdf import (
    load_models_and_build_index,
    retrieve_and_rerank,
    generate_answer
)


st.set_page_config(
    page_title="Michael Jackson RAG Chatbot",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top center, rgba(255, 0, 0, 0.28), transparent 30%),
            radial-gradient(circle at bottom right, rgba(245, 215, 110, 0.22), transparent 35%),
            linear-gradient(135deg, #020202 0%, #170000 45%, #000000 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    .block-container {
        background:
            linear-gradient(145deg, rgba(0, 0, 0, 0.94), rgba(55, 0, 0, 0.90), rgba(10, 6, 0, 0.94)) !important;
        border: 1px solid rgba(245, 215, 110, 0.55);
        border-radius: 30px;
        padding: 3rem 4rem !important;
        box-shadow:
            0 0 35px rgba(255, 204, 51, 0.25),
            0 0 70px rgba(180, 0, 0, 0.35);
    }

    .block-container h1 {
        color: #f5d76e !important;
        text-align: center;
        font-size: 3.2rem !important;
        text-shadow:
            0 0 12px rgba(245, 215, 110, 0.75),
            0 0 28px rgba(255, 0, 0, 0.65);
    }

    .block-container h2,
    .block-container h3 {
        color: #ffcc33 !important;
        text-shadow: 0 0 12px rgba(180, 25, 25, 0.55);
    }

    .block-container p,
    .block-container li,
    .block-container label,
    .block-container span {
        color: #fff4d6 !important;
        font-weight: 500;
    }

    .block-container [data-testid="stAlert"] {
        background: rgba(120, 0, 0, 0.55) !important;
        border: 1px solid #c9a227 !important;
        border-radius: 16px !important;
        box-shadow: 0 0 18px rgba(201, 162, 39, 0.30);
    }

    .block-container [data-testid="stExpander"] {
        background: rgba(0, 0, 0, 0.55) !important;
        border: 1px solid rgba(245, 215, 110, 0.45) !important;
        border-radius: 16px !important;
    }

    .block-container .stButton > button {
        background: linear-gradient(135deg, #1a0000 0%, #050505 100%) !important;
        color: #f5d76e !important;
        border: 1px solid #c9a227 !important;
        border-radius: 14px !important;
        box-shadow: 0 0 18px rgba(201, 162, 39, 0.35);
        font-weight: 800 !important;
    }

    .block-container .stButton > button p {
        color: #f5d76e !important;
        font-weight: 800 !important;
    }

    .block-container .stButton > button:hover {
        background: linear-gradient(135deg, #4a0000 0%, #130000 100%) !important;
        box-shadow: 0 0 28px rgba(255, 204, 51, 0.75);
    }

    .block-container input {
        background: #fff4d6 !important;
        color: #111111 !important;
        border: 1px solid #f5d76e !important;
        border-radius: 14px !important;
    }

    .block-container [data-testid="stChatMessage"] {
        background: rgba(0, 0, 0, 0.45) !important;
        border: 1px solid rgba(245, 215, 110, 0.25);
        border-radius: 18px;
        padding: 1rem;
    }

    hr {
        border-color: rgba(245, 215, 110, 0.45) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("assets/mj_logo.png", width=240)

st.title("Michael Jackson RAG Chatbot")
st.caption("Ask questions using a PDF-based knowledge base.")

st.divider()

st.subheader("Knowledge Base")
st.info(
    "This chatbot uses PDF documents about Michael Jackson. "
    "It extracts text from PDFs, splits it into chunks, creates embeddings, "
    "searches relevant information with FAISS, reranks the results, "
    "and generates an answer with an LLM."
)

with st.expander("PDF documents used in this project"):
    st.markdown("- Michael_Jackson_as_a_mythical_hero_.pdf")
    st.markdown("- The_Legacy_of_Michael_Jackson.pdf")
    st.markdown("- michael-jackson-king-of-pops-darkest-hour.pdf")


@st.cache_resource
def load_rag():
    with st.spinner("Loading RAG assistant..."):
        return load_models_and_build_index()


try:
    rag_components = load_rag()

    if "mj_messages" not in st.session_state:
        st.session_state.mj_messages = [
            {
                "role": "assistant",
                "content": "Hi! Ask me about Michael Jackson using the PDF knowledge base."
            }
        ]

    for message in st.session_state.mj_messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict):
                st.markdown(message["content"]["answer"])

                with st.expander("Retrieved sources"):
                    for chunk in message["content"]["context"]:
                        st.markdown(f"**Source:** {chunk['source']}")
                        st.write(chunk["text"][:500] + " ... [source text shortened]")
            else:
                st.markdown(message["content"])


    def handle_user_query(prompt):
        st.session_state.mj_messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching PDF documents..."):
                context = retrieve_and_rerank(prompt, rag_components)

                answer = generate_answer(
                    prompt,
                    context,
                    groq_client=rag_components["groq_client"]
                )

            st.markdown(answer)

            with st.expander("Retrieved sources"):
                for chunk in context:
                    st.markdown(f"**Source:** {chunk['source']}")
                    st.write(chunk["text"][:500] + " ... [source text shortened]")

        st.session_state.mj_messages.append({
            "role": "assistant",
            "content": {
                "answer": answer,
                "context": context
            }
        })


    st.markdown("### Example questions")

    col1, col2 = st.columns(2)

    if col1.button("Why is Michael Jackson described as a mythical hero?"):
        handle_user_query("Why is Michael Jackson described as a mythical hero?")

    if col2.button("What is Michael Jackson's legacy?"):
        handle_user_query("What is Michael Jackson's legacy?")

    if st.button("What happened during Michael Jackson's darkest hour?"):
        handle_user_query("What happened during Michael Jackson's darkest hour?")

    st.markdown("### Ask your own question")

    with st.form("rag_question_form"):
        user_question = st.text_input(
            "Type your question:",
            placeholder="Ask something based on the PDF documents...",
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button("Ask RAG Chatbot")

    if submitted:
        if user_question.strip():
            handle_user_query(user_question)
        else:
            st.warning("Please type a question first.")


except Exception as e:
    st.error("RAG chatbot is not ready yet.")
    st.write(e)
    st.info(
        "Check that the PDF files are inside rag_articles/ "
        "and that GROQ_API_KEY is set in Streamlit secrets."
    )

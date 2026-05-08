import streamlit as st

from rag_logic_mj import (
    load_models_and_build_index,
    retrieve_and_rerank,
    generate_answer
)


st.set_page_config(
    page_title="Michael Jackson RAG Chatbot",
    layout="centered"
)

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
                "content": (
                    "Hi! Ask me about Michael Jackson using the PDF knowledge base."
                )
            }
        ]

    for message in st.session_state.mj_messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict):
                st.markdown(message["content"]["answer"])

                with st.expander("Retrieved sources"):
                    for chunk in message["content"]["context"]:
                        st.markdown(f"**Source:** {chunk['source']}")
                        st.write(chunk["text"])
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
                    st.write(chunk["text"])

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

    user_question = st.text_input(
        "Type your question:",
        placeholder="Ask something based on the PDF documents...",
        label_visibility="collapsed"
    )

    if st.button("Ask RAG Chatbot"):
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

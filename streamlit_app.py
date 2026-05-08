import streamlit as st
import pandas as pd
from streamlit_player import st_player
from rag_logic_mj import load_models_and_build_index, retrieve_and_rerank, generate_answer

st.set_page_config(
    page_title="Michael Jackson Project",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load data
df = pd.read_csv("data/michael_jackson_simple.csv")

#link for the dataset:
#https://kworb.net/spotify/artist/3fMbdgg4jU18AjLCKBhRSm_songs.html

# Clean columns
df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
df["daily_streams"] = pd.to_numeric(df["daily_streams"], errors="coerce")

df = df.dropna(subset=["rank", "streams", "daily_streams"])
df["rank"] = df["rank"].astype(int)
df["streams"] = df["streams"].astype(int)
df["daily_streams"] = df["daily_streams"].astype(int)

min_rank = int(df["rank"].min())
max_rank = int(df["rank"].max())

# Sidebar
with st.sidebar:
    st.title("Michael Jackson")
    st.info("Choose song rank")

    selected_rank = st.slider(
        "Choose rank:",
        min_value=min_rank,
        max_value=max_rank,
        value=min_rank,
        step=1
    )

    filtered = df[df["rank"] == selected_rank]

    st.divider()

    if not filtered.empty:
        song = filtered.iloc[0]

        st.subheader(f"Rank #{selected_rank}")
        st.success(song["name"])

        st.metric("Daily Streams", f"{song['daily_streams']:,}")
        st.metric("Total Streams", f"{song['streams']:,}")

    else:
        song = None
        st.warning("No song found for this rank.")

# Main page
st.title("Michael Jackson Song Finder")
st.info("Choose a rank from the left sidebar and find the most popular Michael Jackson song.")

if song is not None:
    st.subheader(f"Michael Jackson - Don't Stop 'Til You Get Enough")

    st_player("https://www.youtube.com/watch?v=yURRmWtbTbo")


st.divider()
st.header("Ask about Michael Jackson")
st.caption("The chatbot answers using article sources and shows links.")

@st.cache_resource
def load_rag():
    with st.spinner("Loading Michael Jackson RAG assistant..."):
        return load_models_and_build_index()

try:
    rag_components = load_rag()

    if "mj_messages" not in st.session_state:
        st.session_state.mj_messages = [
            {
                "role": "assistant",
                "content": "Hi! Ask me about Michael Jackson's biography, songs, albums, awards, or influence."
            }
        ]

    for message in st.session_state.mj_messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict):
                st.markdown(message["content"]["answer"])

                with st.expander("Sources"):
                    for chunk in message["content"]["context"]:
                        st.markdown(f"**Source:** [{chunk['source']}]({chunk['url']})")
                        st.write(chunk["text"])
            else:
                st.markdown(message["content"])

    def handle_user_query(prompt):
        st.session_state.mj_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching sources..."):
                context = retrieve_and_rerank(prompt, rag_components)
                answer = generate_answer(
                    prompt,
                    context,
                    groq_client=rag_components["groq_client"]
                )

            st.markdown(answer)

            with st.expander("Sources"):
                for chunk in context:
                    st.markdown(f"**Source:** [{chunk['source']}]({chunk['url']})")
                    st.write(chunk["text"])

        st.session_state.mj_messages.append({
            "role": "assistant",
            "content": {
                "answer": answer,
                "context": context
            }
        })

    col1, col2, col3 = st.columns(3)

    if col1.button("Who was Michael Jackson?"):
        handle_user_query("Who was Michael Jackson?")

    if col2.button("What made Thriller important?"):
        handle_user_query("What made Thriller important?")

    if col3.button("How many GRAMMYs did he win?"):
        handle_user_query("How many GRAMMYs did Michael Jackson win?")

    if prompt := st.chat_input("Ask something about Michael Jackson..."):
        handle_user_query(prompt)

except Exception as e:
    st.error("RAG chatbot is not ready yet.")
    st.write(e)
    st.info("Check that data/mj_articles.csv exists and GROQ_API_KEY is set.")

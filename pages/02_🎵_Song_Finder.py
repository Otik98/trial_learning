import streamlit as st
import pandas as pd
from streamlit_player import st_player
from rag_logic_mj import load_models_and_build_index, retrieve_and_rerank, generate_answer

st.set_page_config(
    page_title="Michael Jackson Project",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Background behind main content */
    .stApp {
        background:
            radial-gradient(circle at top center, rgba(255, 0, 0, 0.35), transparent 30%),
            radial-gradient(circle at bottom right, rgba(245, 215, 110, 0.28), transparent 35%),
            linear-gradient(135deg, #020202 0%, #170000 45%, #000000 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    /* Main card */
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

    /* Titles */
    .block-container h1 {
        color: #f5d76e !important;
        text-align: center;
        font-size: 3.5rem !important;
        text-shadow:
            0 0 12px rgba(245, 215, 110, 0.75),
            0 0 28px rgba(255, 0, 0, 0.65);
    }

    .block-container h2,
    .block-container h3 {
        color: #ffcc33 !important;
        text-shadow: 0 0 12px rgba(180, 25, 25, 0.55);
    }

    /* Text */
    .block-container p,
    .block-container li,
    .block-container label {
        color: #fff4d6 !important;
        font-weight: 500;
    }

    .block-container a {
        color: #ffd84d !important;
        font-weight: 800;
    }

    /* YouTube player */
    .block-container iframe {
        border: 2px solid #c9a227 !important;
        border-radius: 22px !important;
        box-shadow:
            0 0 25px rgba(245, 215, 110, 0.45),
            0 0 55px rgba(180, 0, 0, 0.55);
    }

    /* Alerts / info boxes */
    .block-container [data-testid="stAlert"] {
        background: rgba(120, 0, 0, 0.55) !important;
        border: 1px solid #c9a227 !important;
        border-radius: 16px !important;
        box-shadow: 0 0 18px rgba(201, 162, 39, 0.30);
    }

    /* Expander */
    .block-container [data-testid="stExpander"] {
        background: rgba(0, 0, 0, 0.55) !important;
        border: 1px solid rgba(245, 215, 110, 0.45) !important;
        border-radius: 16px !important;
    }

    /* Question buttons */
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

    /* Chat input */
    .block-container [data-testid="stChatInput"] {
        background: rgba(0, 0, 0, 0.65) !important;
        border: 1px solid rgba(245, 215, 110, 0.55) !important;
        border-radius: 18px !important;
        box-shadow: 0 0 18px rgba(201, 162, 39, 0.35);
    }

    .block-container [data-testid="stChatInput"] textarea {
        color: #111827 !important;
    }

    hr {
        border-color: rgba(245, 215, 110, 0.45) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("assets/mj_logo.png", width=240)

st.sidebar.markdown(
    '<div class="mj-glow">Michael<br>Jackson</div>',
    unsafe_allow_html=True
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


youtube_links = {
    1: "https://www.youtube.com/watch?v=Zi_XLOBDo_Y",
    2: "https://www.youtube.com/watch?v=oRdxUFDoQe0",
    3: "https://www.youtube.com/watch?v=h_D3VFfhvs4",
    4: "https://www.youtube.com/watch?v=sOnqjkJTMaA",
    5: "https://www.youtube.com/watch?v=5X-Mrc2l1d0",
    6: "https://www.youtube.com/watch?v=yURRmWtbTbo",
    7: "https://www.youtube.com/watch?v=HzZ_urpj4As",
    8: "https://www.youtube.com/watch?v=Y_8mUx4VOmo",
    9: "https://www.youtube.com/watch?v=PivWY9wn5ps",
    10: "https://www.youtube.com/watch?v=1ZZQuj6htF4"
}

st.title("Michael Jackson Song Finder")

if song is not None:
    st.subheader(f"Michael Jackson - {song['name']}")

    video_url = youtube_links.get(selected_rank)

    if video_url:
        st_player(video_url)
    else:
        st.warning("No video available for this rank yet.")

st.divider()
st.subheader("Project data sources")

st.markdown(
    "- **Spotify artist page:** "
    "[Michael Jackson on Spotify](https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm)"
)

st.markdown(
    "- **Spotify ranking and streams:** "
    "[Kworb — Michael Jackson Spotify Songs](https://kworb.net/spotify/artist/3fMbdgg4jU18AjLCKBhRSm_songs.html)"
)

st.markdown(
    "- **Song/video data:** YouTube official Michael Jackson videos and Spotify stream ranking."
)

articles = pd.read_csv("data/mj_articles.csv")

with st.expander("Sources used by the chatbot"):
    for _, row in articles[["title", "url"]].drop_duplicates().iterrows():
        st.markdown(f"- [{row['title']}]({row['url']})")

        

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

    st.markdown("### Ask your own question")

    user_question = st.text_input(
        "Type your question:",
        placeholder="Ask something about Michael Jackson...",
        label_visibility="collapsed")


    if st.button("Ask Michael Bot"):
         if user_question.strip():
             handle_user_query(user_question)
         else:
             st.warning("Please type a question first.")
        
    #if prompt := st.chat_input("Ask something about Michael Jackson..."):
     #   handle_user_query(prompt)

except Exception as e:
    st.error("RAG chatbot is not ready yet.")
    st.write(e)
    st.info("Check that data/mj_articles.csv exists and GROQ_API_KEY is set.")

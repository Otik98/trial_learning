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


import streamlit as st
import pandas as pd
from streamlit_player import st_player

st.set_page_config(
    page_title="Michael Jackson Project",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
df = pd.read_csv("data/michael_jackson_simple.csv")

# Clean columns
df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
df["daily_streams"] = pd.to_numeric(df["daily_streams"], errors="coerce")

df = df.dropna(subset=["rank", "streams", "daily_streams"])
df["rank"] = df["rank"].astype(int)
df["streams"] = df["streams"].astype(int)
df["daily_streams"] = df["daily_streams"].astype(int)

# Sidebar
st.sidebar.title("Michael Jackson")
st.sidebar.info("Choose song rank")

min_rank = int(df["rank"].min())
max_rank = int(df["rank"].max())

selected_rank = st.sidebar.slider(
    "Choose rank:",
    min_value=min_rank,
    max_value=max_rank,
    value=min_rank,
    step=1
)

# Main page
st.title("Michael Jackson Song Finder")
st.info("Choose a rank from the left sidebar and find the most popular Michael Jackson song.")

filtered = df[df["rank"] == selected_rank]

if not filtered.empty:
    song = filtered.iloc[0]

    st.subheader(f"Rank #{selected_rank}")
    st.success(song["name"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Daily Streams", f"{song['daily_streams']:,}")

    with col2:
        st.metric("Total Streams", f"{song['streams']:,}")

    st.subheader(f"Michael Jackson - {song['name']}")

    st_player("https://www.youtube.com/watch?v=yURRmWtbTbo")

else:
    st.warning("No song found for this rank.")

with st.expander("Show full dataset"):
    st.dataframe(df)

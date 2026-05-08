import streamlit as st
import pandas as pd
from streamlit_player import st_player

st.set_page_config(page_title="Michael Jackson Project", layout="wide")

st.title("Michael Jackson Song Finder")
st.info("Choose a rank and find the most popular Michael Jackson song from the dataset.")

df = pd.read_csv("data/michael_jackson_simple.csv")

# Clean columns
df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["daily_streams"] = pd.to_numeric(df["daily_streams"], errors="coerce")

df = df.dropna(subset=["rank", "daily_streams"])
df["rank"] = df["rank"].astype(int)
df["daily_streams"] = df["daily_streams"].astype(int)

# Unique ranks only
ranks = sorted(df["rank"].unique())

selected_rank = st.select_slider(
    "Choose rank:",
    options=ranks
)

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

else:
    st.warning("No song found for this rank.")

with st.expander("Show full dataset"):
    st.dataframe(df)

st.subheader("Michael Jackson - Billie Jean")

st_player("https://www.youtube.com/watch?v=Zi_XLOBDo_Y")

import streamlit as st

st.title('Michael Jackson')

st.info('This is trial bot for the MJ bio')

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Michael Jackson Project", layout="centered")

st.title("Michael Jackson Song Finder")
st.info("Choose a rank and find the most popular Michael Jackson song from the dataset.")

df = pd.read_csv("data/michael_jackson_simple.csv")

# Clean columns
df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
df["daily_streams"] = pd.to_numeric(df["daily_streams"], errors="coerce")
df = df.dropna(subset=["rank", "daily_streams"])
df["rank"] = df["rank"].astype(int)

# Unique ranks only
ranks = sorted(df["rank"].unique())

selected_rank = st.select_slider(
    "Choose rank:",
    options=ranks
)

filtered = df[df["rank"] == selected_rank]

#if not filtered.empty:
#    best_song = filtered.sort_values("daily_streams", ascending=False).iloc[0]

#    st.subheader(f"Best song in {selected_rank}")

#    st.success(best_song["Title"])

#    col1, col2 = st.columns(2)

#    with col1:
#        st.metric("Daily Streams", int(best_song["daily_streams"]))
#
#    with col2:
#        st.metric("Rank", selected_rank)
#
#    st.write("Artist:", best_song["Artist"])

#else:
#    st.warning("No song found for this rank.")

#with st.expander("Show full dataset"):
#    st.dataframe(df)


from streamlit_player import st_player

st_player('https://www.youtube.com/watch?v=yURRmWtbTbo&list=RDyURRmWtbTbo&start_radio=1')

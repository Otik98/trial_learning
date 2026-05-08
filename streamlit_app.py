import streamlit as st

st.title('Michael Jackson')

st.info('This is trial bot for the MJ bio')


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Michael Jackson Project", layout="wide")

st.title("Michael Jackson Song Popularity Analysis")

st.info("This app analyzes Michael Jackson songs using a Spotify dataset.")

df = pd.read_csv("data/michael_jackson_simple.csv")

st.subheader("Dataset")
st.dataframe(df)

st.write(f"Number of songs in dataset: {len(df)}")

st.subheader("Top songs by popularity")

top_songs = df.sort_values("Popularity", ascending=False)

st.dataframe(top_songs[["Title", "Year", "Popularity"]])

st.bar_chart(top_songs.set_index("Title")["Popularity"])

st.subheader("Find the most popular song by year")

year = st.selectbox("Choose year", sorted(df["Year"].unique()))

filtered = df[df["Year"] == year]

st.dataframe(filtered[["Title", "Year", "Popularity"]])

if not filtered.empty:
    best_song = filtered.sort_values("Popularity", ascending=False).iloc[0]
    st.success(
        f"Most popular song in {year}: {best_song['Title']} "
        f"with popularity {best_song['Popularity']}"
    )

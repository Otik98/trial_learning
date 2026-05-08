import streamlit as st

st.title('Michael Jackson')

st.info('This is trial bot for the MJ bio')

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Michael Jackson Project", layout="centered")

st.title("Michael Jackson Song Finder")
st.info("Choose a year and find the most popular Michael Jackson song from the dataset.")

df = pd.read_csv("data/michael_jackson_simple.csv")

# Clean columns
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Popularity"] = pd.to_numeric(df["Popularity"], errors="coerce")
df = df.dropna(subset=["Year", "Popularity"])
df["Year"] = df["Year"].astype(int)

# Unique years only
years = sorted(df["Year"].unique())

selected_year = st.select_slider(
    "Choose year:",
    options=years
)

filtered = df[df["Year"] == selected_year]

if not filtered.empty:
    best_song = filtered.sort_values("Popularity", ascending=False).iloc[0]

    st.subheader(f"Best song in {selected_year}")

    st.success(best_song["Title"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Popularity", int(best_song["Popularity"]))

    with col2:
        st.metric("Year", selected_year)

    st.write("Artist:", best_song["Artist"])

else:
    st.warning("No song found for this year.")

with st.expander("Show full dataset"):
    st.dataframe(df)

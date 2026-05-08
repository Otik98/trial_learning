import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Grammy Winners",
    layout="centered",
    initial_sidebar_state="expanded"
)



st.sidebar.image("assets/mj_logo.png", width=160)

st.title("Grammy Winners Explorer")
st.info("Explore Grammy Big Four winners from 1959 to 2026.")

df = pd.read_csv("data/grammy_big_four.csv")

# Clean columns
df.columns = df.columns.str.strip()

# Keep only winners
df = df[df["Status"] == "Winner"]

# Clean year
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)

# Remove exact duplicates
df = df.drop_duplicates(
    subset=["Year", "Category", "Winner", "Artist"]
)

# Sidebar controls
st.sidebar.header("Grammy Explorer")

selected_year = st.sidebar.slider(
    "Choose Grammy year:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=1984,
    step=1
)

categories = sorted(df["Category"].dropna().unique())

selected_category = st.sidebar.selectbox(
    "Choose category:",
    categories
)

filtered = df[
    (df["Year"] == selected_year) &
    (df["Category"] == selected_category)
]

st.subheader(f"{selected_category} — {selected_year}")

if not filtered.empty:
    for _, row in filtered.iterrows():

        if row["Category"] == "Song of the Year":
            display_winner = str(row["Artist"]).replace('" *', '').replace('"', '')
            display_artist = str(row["Winner"]).replace(
                "Michael JacksonLionel Richie",
                "Michael Jackson, Lionel Richie"
            )
        else:
            display_winner = row["Winner"]
            display_artist = row["Artist"]

        st.success(display_winner)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Artist / Creator", display_artist)

        with col2:
            st.metric("Ceremony", f"{int(row['Ceremony_Number'])}th")

        st.write("**Era:**", row["Era"])

        st.markdown(
            "**Dataset source:** "
            "[Kaggle — Grammy Award Winners 1959–2026]"
            "(https://www.kaggle.com/datasets/mafaqbhatti/grammy-award-winners-1959-2026/data)"
        )

        st.write("**Original source in dataset:**", row["Data_Source"])

else:
    st.warning("No winner found for this year/category.")
    
st.divider()

st.subheader("Michael Jackson Grammy highlight")

mj_rows = df[
    df["Artist"].astype(str).str.contains("Michael Jackson", case=False, na=False) |
    df["Winner"].astype(str).str.contains("Michael Jackson", case=False, na=False)
]

if not mj_rows.empty:
    mj_display = mj_rows[["Year", "Category", "Winner", "Artist", "Ceremony_Number"]].copy()

    # Fix display for Song of the Year rows
    mask = mj_display["Category"] == "Song of the Year"

    mj_display.loc[mask, "Winner"] = (
        mj_display.loc[mask, "Artist"]
        .astype(str)
        .str.replace('" *', '', regex=False)
        .str.replace('"', '', regex=False)
    )

    mj_display.loc[mask, "Artist"] = (
        mj_display.loc[mask, "Artist"]
        .astype(str)
        .replace("We Are the World\" *", "Michael Jackson, Lionel Richie")
    )

    # Specific clean-up for this dataset row
    mj_display.loc[
        (mj_display["Year"] == 1986) & (mj_display["Category"] == "Song of the Year"),
        "Artist"
    ] = "Michael Jackson, Lionel Richie"

    st.dataframe(
        mj_display,
        use_container_width=True
    )
else:
    st.info("No Michael Jackson rows found in this dataset.")



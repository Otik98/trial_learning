import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Grammy Winners",
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



import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Michael Jackson Biography",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top, rgba(180, 25, 25, 0.35), transparent 35%),
            linear-gradient(135deg, #050505 0%, #120000 45%, #1a0f00 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #160000 55%, #2b1a00 100%);
        border-right: 2px solid #c9a227;
    }

    h1 {
        color: #f5d76e !important;
        text-shadow: 2px 2px 8px rgba(255, 0, 0, 0.45);
    }

    h2, h3 {
        color: #f2c94c !important;
    }

    p, li, span, div, label {
        color: #f7f1df !important;
    }

    .stAlert {
        background-color: rgba(120, 0, 0, 0.35) !important;
        border: 1px solid #c9a227 !important;
        border-radius: 12px;
    }

    [data-testid="stTable"] {
        background-color: rgba(0, 0, 0, 0.45);
        border: 1px solid #c9a227;
        border-radius: 12px;
    }

    a {
        color: #ffcc33 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar logo
st.sidebar.image("assets/mj_logo.png", width=240)

# Main page
st.title("Michael Jackson Biography")

st.image("mj_1988.jpg", width=320)

st.markdown(
    "Photo: [Michael Jackson in 1988](https://commons.wikimedia.org/wiki/File:Michael_Jackson_in_1988.jpg) "
    "by Zoran Veselinovic, licensed under "
    "[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)."
)

st.header("Who was Michael Jackson?")

st.markdown(
    """
    **Michael Jackson** was an American singer, songwriter, dancer, and performer.
    He became one of the most influential artists in popular music and is often
    called the **King of Pop**.

    He was born in **Gary, Indiana, in 1958** and first became famous as a child
    performer with **The Jackson 5**. Later, he became a global solo artist with
    albums such as **Off the Wall**, **Thriller**, **Bad**, **Dangerous**, and
    **HIStory**.

    Michael Jackson was known for his unique voice, dance style, stage presence,
    music videos, and global influence on pop culture.
    """
)

st.header("Career highlights")

timeline = pd.DataFrame(
    {
        "Year": [1958, 1960, 1979, 1982, 1987, 1991, 1995, 2009],
        "Event": [
            "Born in Gary, Indiana",
            "Started performing with his brothers in The Jackson 5 era",
            "Released Off the Wall",
            "Released Thriller",
            "Released Bad",
            "Released Dangerous",
            "Released HIStory",
            "Died in 2009, leaving a major musical legacy",
        ],
    }
)

st.table(timeline)

st.header("Musical influence")

st.markdown(
    """
    Michael Jackson helped change the role of music videos in popular music.
    His videos for songs such as **Thriller**, **Billie Jean**, **Beat It**,
    and **Smooth Criminal** became important parts of pop culture.

    He also influenced dance and stage performance through moves such as the
    **moonwalk**, sharp choreography, and theatrical live shows.
    """
)

st.header("Famous songs")

st.markdown(
    """
    Some of his most famous songs include:

    - **Billie Jean**
    - **Beat It**
    - **Thriller**
    - **Smooth Criminal**
    - **Black or White**
    - **Man in the Mirror**
    - **The Way You Make Me Feel**
    - **Don't Stop 'Til You Get Enough**
    """
)

st.header("Sources")

st.markdown(
    """
    - [Michael Jackson Official Website](https://www.michaeljackson.com/)
    - [Michael Jackson on Spotify](https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm)
    - [Britannica Biography](https://www.britannica.com/biography/Michael-Jackson)
    - [GRAMMY Profile](https://www.grammy.com/artists/michael-jackson/13202)
    - [Rock & Roll Hall of Fame](https://rockhall.com/inductees/michael-jackson/)
    """
)

st.divider()

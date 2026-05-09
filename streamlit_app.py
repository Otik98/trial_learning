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
    /* Main page background only */
    [data-testid="stMain"] {
        background:
            radial-gradient(circle at top, rgba(180, 25, 25, 0.35), transparent 35%),
            linear-gradient(135deg, #050505 0%, #120000 45%, #1a0f00 100%);
    }

    /* Main content card */
    [data-testid="stMainBlockContainer"] {
        background: rgba(0, 0, 0, 0.25);
        border-radius: 22px;
        padding: 3rem 4rem;
    }

    /* Header transparent */
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    /* Text only inside main page */
    [data-testid="stMain"] h1 {
        color: #f5d76e !important;
        text-shadow: 2px 2px 10px rgba(255, 0, 0, 0.55);
    }

    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3 {
        color: #ffcc33 !important;
    }

    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] label {
        color: #f7f1df !important;
    }

    [data-testid="stMain"] a {
        color: #ffcc33 !important;
    }

    /* Tables inside main page */
    [data-testid="stMain"] table {
        color: #f7f1df !important;
    }

    [data-testid="stMain"] th,
    [data-testid="stMain"] td {
        color: #f7f1df !important;
    }
        .hero-subtitle {
        color: #ffcc33;
        font-size: 1.35rem;
        font-weight: 600;
        margin-top: -0.5rem;
        margin-bottom: 0.8rem;
        text-shadow: 1px 1px 8px rgba(255, 204, 51, 0.35);
    }

    .hero-description {
        color: #f7f1df;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 720px;
        margin-bottom: 1.2rem;
    }

    .signature-line {
        color: #f5d76e;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 1.5rem;
    }

    .feature-card {
        background: rgba(255, 204, 51, 0.08);
        border: 1px solid rgba(255, 204, 51, 0.35);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .feature-card h4 {
        color: #ffcc33;
        margin-bottom: 0.3rem;
    }

    .feature-card p {
        color: #f7f1df;
        font-size: 0.95rem;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar logo
st.sidebar.image("assets/mj_logo.png", width=240)

# Main page
st.title("Michael Jackson Biography")

st.markdown(
    """
    <div class="hero-subtitle">
        The King of Pop Experience
    </div>

    <div class="hero-description">
        Step into the world of Michael Jackson and explore his life, music,
        performances, achievements, and legacy through an interactive Streamlit experience.
    </div>

    <div class="signature-line">
        Music. Dance. Legacy.
    </div>
    """,
    unsafe_allow_html=True
)

st.image("mj_1988.jpg", width=320)

st.markdown(
    "Photo: [Michael Jackson in 1988](https://commons.wikimedia.org/wiki/File:Michael_Jackson_in_1988.jpg) "
    "by Zoran Veselinovic, licensed under "
    "[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)."
)

st.markdown("### What can you explore here?")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>Biography</h4>
            <p>Learn about Michael Jackson’s life, career, and global influence.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">
            <h4>Famous Songs</h4>
            <p>Discover some of his most iconic songs and albums.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>Music Data</h4>
            <p>Explore song information, rankings, and music-related data.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">
            <h4>Chatbot</h4>
            <p>Ask questions and interact with a simple knowledge-based chatbot.</p>
        </div>
        """,
        unsafe_allow_html=True
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

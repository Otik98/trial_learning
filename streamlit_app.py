import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Michael Jackson Biography",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Michael Jackson Biography")

st.info(
    "This page presents a short biography of Michael Jackson. "
    "Use the sidebar to open the Song Finder and chatbot page."
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

st.success(
    "Open the Song Finder page from the sidebar to explore songs, streams, videos, and the chatbot."
)

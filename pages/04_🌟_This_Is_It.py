import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="This Is It",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.image("assets/mj_logo.png", width=240)

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

image_path = Path("assets/Michael_Jackson_1984_(cropped).jpg")

if not image_path.exists():
    st.error("Image not found. Check the file name in assets folder.")
    st.stop()

mj_image = image_to_base64(image_path)

st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at center, rgba(245, 215, 110, 0.22), transparent 28%),
        radial-gradient(circle at bottom, rgba(180, 0, 0, 0.28), transparent 35%),
        linear-gradient(135deg, #020202 0%, #170000 45%, #050505 100%);
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}

.block-container {
    padding-top: 60px;
}

.final-box {
    text-align: center;
    padding: 55px 40px;
    border: 1px solid rgba(245, 215, 110, 0.5);
    border-radius: 30px;
    background: rgba(0, 0, 0, 0.58);
    box-shadow:
        0 0 35px rgba(255, 204, 51, 0.25),
        0 0 70px rgba(180, 0, 0, 0.35);
}

.final-photo {
    width: 260px;
    border-radius: 26px;
    border: 2px solid rgba(245, 215, 110, 0.75);
    box-shadow:
        0 0 25px rgba(245, 215, 110, 0.35),
        0 0 55px rgba(180, 0, 0, 0.45);
    margin-bottom: 30px;
}

.final-title {
    color: #f5d76e;
    font-size: 4.5rem;
    font-weight: 900;
    text-shadow:
        0 0 12px rgba(245, 215, 110, 0.85),
        0 0 30px rgba(255, 0, 0, 0.65);
    margin-bottom: 25px;
}

.final-text {
    color: #fff4d6;
    font-size: 1.4rem;
    line-height: 1.7;
}

.final-small {
    color: #ffcc33;
    font-size: 1.2rem;
    margin-top: 35px;
    font-weight: 700;
}

.photo-credit {
    color: rgba(255, 244, 214, 0.65);
    font-size: 0.85rem;
    margin-top: 18px;
}
</style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
<div class="final-box"><img class="final-photo" src="data:image/jpeg;base64,{mj_image}" alt="Michael Jackson photo"/><div class="final-title">This Is It</div><div class="final-text">Это финальная страница моего проекта.<br>Спасибо за этот курс, за полученные знания и за возможность применить новые навыки на практике.</div><div class="final-small">Keep the music alive ✨</div><div class="final-quote">“This is our last and final tour...<br>You’ve all been wonderful, and we love you all.”<br><span>— Michael Jackson, Victory Tour, 1984</span></div><div class="photo-credit">Photo: White House Photo Office / Wikimedia Commons, Public Domain</div></div>
    """,
    unsafe_allow_html=True
)

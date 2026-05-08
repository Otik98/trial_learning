import streamlit as st
import base64

st.set_page_config(
    page_title="This Is It",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.image("assets/mj_logo.png", width=240)

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

mj_image = image_to_base64("assets/Michael_Jackson_1984_(cropped).jpg")


st.markdown(
f"""
<div class="final-box">
    <img class="final-photo" src="data:image/jpeg;base64,{mj_image}" alt="Michael Jackson photo"/>

    <div class="final-title">This Is It</div>

    <div class="final-text">
        Это финальная страница моего проекта.<br>
        Спасибо за этот курс, за полученные знания и за возможность применить новые навыки на практике.
    </div>

    <div class="final-small">
        Keep the music alive ✨
    </div>

    <div class="photo-credit">
        Photo: White House Photo Office / Wikimedia Commons, Public Domain
    </div>
</div>
""",
unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="final-box">
        <img class="final-photo" src="data:image/jpeg;base64,{mj_image}">
        
        <div class="final-title">This Is It</div>
        
        <div class="final-text">
            Это финальная страница моего проекта.<br>
            Спасибо за этот курс, за полученные знания и за возможность применить новые навыки на практике.
        </div>

        <div class="final-small">
            Keep the music alive ✨
        </div>

        <div class="photo-credit">
            Photo: White House Photo Office / Wikimedia Commons, Public Domain
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

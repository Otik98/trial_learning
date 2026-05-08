import streamlit as st

st.set_page_config(
    page_title="This Is It",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.image("assets/mj_logo.png", width=240)

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

    .final-box {
        text-align: center;
        margin-top: 120px;
        padding: 70px 40px;
        border: 1px solid rgba(245, 215, 110, 0.5);
        border-radius: 30px;
        background: rgba(0, 0, 0, 0.55);
        box-shadow:
            0 0 35px rgba(255, 204, 51, 0.25),
            0 0 70px rgba(180, 0, 0, 0.35);
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
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="final-box">
        <div class="final-title">This Is It</div>
        <div class="final-text">
            Это финальная страница моего проекта.<br>
            Спасибо за этот курс, за знания и за возможность создать свой сайт.
        </div>
        <div class="final-small">
            The King of Pop never really leaves the stage.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

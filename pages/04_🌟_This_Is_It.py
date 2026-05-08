import streamlit as st

st.set_page_config(
    page_title="This Is It",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.image("assets/mj_logo.png", width=240)

st.title("This Is It")

st.markdown("Это финальная страница моего проекта.")

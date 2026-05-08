# 🎤 Michael Jackson Streamlit Project

Финальный проект по программе **ТехОрда** в школе **DataGroup**.  
Курс: **Data Science**  
Преподаватель: **Zhanerke**  
Дата сдачи проекта: **09.05.2026**

## 📌 Описание проекта

Этот проект представляет собой интерактивный Streamlit-сайт, посвящённый **Michael Jackson**.

Идея проекта появилась после просмотра фильма **Michael biopic**. После этого захотелось создать небольшой сайт, где можно объединить биографию Michael Jackson, популярные песни, данные Spotify, Grammy winners и простой RAG-чатбот.

Проект показывает навыки работы с:

- Python
- Streamlit
- Pandas
- CSV-данными
- визуальным оформлением сайта
- мультимедиа-контентом
- простым chatbot/RAG-подходом
- GitHub и Streamlit Cloud

## 🌐 Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trial-learning.streamlit.app/)

## 🧩 Страницы приложения

### 1. Biography

На первой странице представлена краткая биография Michael Jackson, его музыкальное влияние, важные события карьеры и известные песни.

### 2. Song Finder

На этой странице можно выбрать рейтинг песни Michael Jackson и увидеть:

- название песни
- rank
- daily streams
- total streams
- YouTube video
- источники данных
- chatbot для вопросов о Michael Jackson

### 3. Grammy Winners

Bonus page с данными о победителях Grammy Awards в категориях Big Four с 1959 по 2026 год.

Также отдельно выделены Grammy-моменты, связанные с Michael Jackson.

### 4. This Is It

Финальная страница проекта с короткой благодарностью за курс, знания и возможность применить новые навыки на практике.

## 📊 Использованные данные и источники

### Spotify / Song ranking

- Michael Jackson on Spotify:  
  https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm

- Kworb — Michael Jackson Spotify Songs ranking and streams:  
  https://kworb.net/spotify/artist/3fMbdgg4jU18AjLCKBhRSm_songs.html

### YouTube videos

- Official Michael Jackson VEVO / YouTube videos were used for embedded song previews:  
  https://www.youtube.com/@michaeljacksonVEVO

### Biography and chatbot sources

- Michael Jackson Official Website:  
  https://www.michaeljackson.com/

- Britannica Biography:  
  https://www.britannica.com/biography/Michael-Jackson

- GRAMMY Profile:  
  https://www.grammy.com/artists/michael-jackson/13202

- Rock & Roll Hall of Fame:  
  https://rockhall.com/inductees/michael-jackson/

### Grammy dataset

- Kaggle — Grammy Award Winners 1959–2026:  
  https://www.kaggle.com/datasets/mafaqbhatti/grammy-award-winners-1959-2026/data

### Images

- Michael Jackson 1988 photo, Wikimedia Commons:  
  https://commons.wikimedia.org/wiki/File:Michael_Jackson_in_1988.jpg

- Michael Jackson's star on the Hollywood Walk of Fame, Wikimedia Commons:  
  https://commons.wikimedia.org/wiki/File:1993_walk_of_fame_michael_jackson.jpg

- Michael Jackson silhouette / illustration, Pixabay:  
  https://pixabay.com/illustrations/michael-jackson-the-king-of-pop-1194269/

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Streamlit Player
- Groq API
- GitHub
- Streamlit Cloud

## 📁 Project Structure

```text
trial_learning/
│
├── streamlit_app.py
├── rag_logic_mj.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── michael_jackson_simple.csv
│   ├── mj_articles.csv
│   └── grammy_big_four.csv
│
├── assets/
│   └── mj_logo.png
│
├── pages/
│   ├── 02_🎵_Song_Finder.py
│   ├── 03_🏆_Grammy_Winners.py
│   └── 04_🌟_This_Is_It.py
│
└── mj_1988.jpg

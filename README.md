# DataGroup Final Project

Финальный проект в школе **DataGroup**.
Курс: **Data Science**  
Преподаватель: **Zhanerke**  
Дата сдачи проекта: **09.05.2026**

## 📌 Описание проекта

Этот проект представляет собой интерактивный **Streamlit-сайт**, посвящённый Michael Jackson.

Идея проекта появилась после просмотра фильма **Michael biopic**. После этого захотелось создать небольшой сайт, где можно объединить биографию Michael Jackson, популярные песни, данные Spotify, Grammy winners и RAG-чатбот на основе PDF-документов.

Основная AI-часть проекта — это **RAG-чатбот**, который использует собственную базу знаний из PDF-файлов о Michael Jackson. Чатбот извлекает текст из документов, делит его на фрагменты, создаёт embeddings, ищет релевантную информацию через FAISS и генерирует ответ с помощью LLM.

Дополнительно в проект был добавлен интерактивный Song Finder с данными Spotify и YouTube-видео.

Проект показывает навыки работы с:

- Python
- Streamlit
- Pandas
- NumPy
- CSV-данными
- PDF-документами
- PyMuPDF для извлечения текста из PDF
- Sentence Transformers для embeddings
- FAISS для векторного поиска
- Cross-Encoder для reranking
- Groq API для генерации ответов
- визуальным оформлением сайта
- мультимедиа-контентом
- RAG-подходом
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

Эта страница является интерактивным бонусом к основной RAG-части проекта.

### 3. Grammy Winners

Bonus page с данными о победителях Grammy Awards в категориях Big Four с 1959 по 2026 год.

Также отдельно выделены Grammy-моменты, связанные с Michael Jackson.

### 4. MJ Knowledge Chatbot

Основная AI-страница проекта.

На этой странице реализован **RAG-чатбот**, который отвечает на вопросы о Michael Jackson, используя PDF-документы из собственной базы знаний.

RAG pipeline включает:

- загрузку PDF-документов
- извлечение текста из PDF
- очистку текста
- разбиение текста на chunks
- создание embeddings
- FAISS vector search
- reranking через Cross-Encoder
- генерацию ответа через Groq LLM
- отображение найденных источников

Примеры вопросов:

- Why is Michael Jackson described as a mythical hero?
- What is Michael Jackson's legacy?
- What happened during Michael Jackson's darkest hour?

### 5. This Is It

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

### RAG PDF Knowledge Base

The RAG chatbot uses PDF documents stored in the `rag_articles/` folder:

- `Michael_Jackson_as_a_mythical_hero_.pdf`
- `The_Legacy_of_Michael_Jackson.pdf`
- `michael-jackson-king-of-pops-darkest-hour.pdf`

These PDF documents form the custom knowledge base for the chatbot.

### Biography and additional chatbot sources

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
- PyMuPDF
- Sentence Transformers
- FAISS
- Cross-Encoder
- LangChain Text Splitters
- Groq API
- GitHub
- Streamlit Cloud

## 📁 Project Structure

```text
trial_learning/
│
├── streamlit_app.py
├── rag_logic_mj.py
├── rag_logic_pdf.py
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
├── rag_articles/
│   ├── Michael_Jackson_as_a_mythical_hero_.pdf
│   ├── The_Legacy_of_Michael_Jackson.pdf
│   └── michael-jackson-king-of-pops-darkest-hour.pdf
│
├── pages/
│   ├── 02_🎵_Song_Finder.py
│   ├── 03_🏆_Grammy_Winners.py
│   ├── 04_🤖_MJ_Knowledge_Chatbot.py
│   └── 05_🌟_This_Is_It.py
│
└── mj_1988.jpg

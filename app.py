import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# HARUS PALING ATAS
st.set_page_config(layout="wide")

# Animasi Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_music = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_w51pcehl.json")
st_lottie(lottie_music, height=300, key="music")

# Load dataset
df = pd.read_csv("spotify_songs.csv")
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
df['year'] = df['track_album_release_date'].dt.year

st.title("🎵 Visualisasi Data Spotify")

# Sidebar 
option = st.sidebar.selectbox("Pilih Visualisasi", (
    "1. Genre Musik Favorit Tahun 2020",
    "2. Tren Genre Berdasarkan Tahun",
    "3. Top 10 Artis Populer",
    "4. Danceability vs Popularity",
    "5. Rata-rata Danceability per Genre",
    "6. Distribusi Tempo Lagu",
    "7. Mood Musik per Genre (Barplot)",
    "8. Mood Musik per Genre (Radar Chart)"
))

# 1. Genre Favorit 2020
if option == "1. Genre Musik Favorit Tahun 2020":
    st.header("🎧 Genre Musik Favorit Tahun 2020")
    df_2020 = df[df['year'] == 2020]
    genre_popularity = df_2020.groupby('playlist_genre')['track_popularity'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=genre_popularity.values, y=genre_popularity.index, palette='crest', ax=ax)
    ax.set_title("Popularitas Genre Musik Tahun 2020")
    st.pyplot(fig)

# 2. Tren Genre Berdasarkan Tahun
elif option == "2. Tren Genre Berdasarkan Tahun":
    st.header("📈 Tren Genre Musik dari Tahun ke Tahun")
    trend = df[df['year'] >= 2010].groupby(['year', 'playlist_genre'])['track_popularity'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.lineplot(data=trend, x='year', y='track_popularity', hue='playlist_genre', marker='o', ax=ax)
    ax.set_title("Perubahan Popularitas Genre Musik")
    st.pyplot(fig)

# 3. Top 10 Artis Populer
elif option == "3. Top 10 Artis Populer":
    st.header("🏆 Top 10 Artis Berdasarkan Popularitas Lagu")
    top_artist = df.groupby('track_artist')['track_popularity'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_artist.values, y=top_artist.index, palette='viridis', ax=ax)
    ax.set_title("Top 10 Artis Populer")
    st.pyplot(fig)

# --- 4. Danceability vs Popularity per Genre ---
elif option == "4. Danceability vs Popularity":
    st.subheader("🎚️ Danceability vs Popularity per Genre")

    # Buat mapping warna tetap per genre
    unique_genres = sorted(df['playlist_genre'].dropna().unique())
    palette = sns.color_palette("tab10", len(unique_genres))
    genre_colors = dict(zip(unique_genres, palette))

    # Opsi dropdown
    genre_options = ["Semua Genre"] + unique_genres
    selected_genre = st.selectbox("Pilih Genre", genre_options)

    fig, ax = plt.subplots(figsize=(10, 6))

    if selected_genre == "Semua Genre":
        sns.scatterplot(
            data=df,
            x="danceability",
            y="track_popularity",
            hue="playlist_genre",
            palette=genre_colors,
            alpha=0.6,
            ax=ax
        )
        ax.set_title("Danceability vs Popularity (Semua Genre)")
        ax.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc="upper left")
    else:
        genre_data = df[df['playlist_genre'] == selected_genre]
        sns.scatterplot(
            data=genre_data,
            x="danceability",
            y="track_popularity",
            color=genre_colors[selected_genre],  # Gunakan warna tetap
            alpha=0.6,
            ax=ax
        )
        ax.set_title(f"Danceability vs Popularity ({selected_genre})")
        if ax.legend_:
            ax.legend_.remove()

    ax.set_xlabel("Danceability")
    ax.set_ylabel("Popularity")
    st.pyplot(fig)



# 5. Rata-rata Danceability per Genre
elif option == "5. Rata-rata Danceability per Genre":
    st.header("🎼 Rata-rata Danceability per Genre")
    dance_avg = df.groupby('playlist_genre')['danceability'].mean().sort_values()
    fig, ax = plt.subplots()
    dance_avg.plot(kind='barh', color='mediumseagreen', ax=ax)
    ax.set_xlabel("Danceability")
    ax.set_title("Rata-rata Danceability per Genre")
    st.pyplot(fig)

# 6. Distribusi Tempo Lagu
elif option == "6. Distribusi Tempo Lagu":
    st.header("🎵 Distribusi Tempo Lagu")
    fig, ax = plt.subplots()
    sns.histplot(df["tempo"], kde=True, color="skyblue", bins=30, ax=ax)
    ax.set_title("Distribusi Tempo")
    st.pyplot(fig)

# 7. Mood Musik per Genre (Barplot)
elif option == "7. Mood Musik per Genre (Barplot)":
    st.header("🎶 Mood Musik per Genre (Valence, Energy, dll)")
    mood_cols = ["valence", "energy", "acousticness", "danceability", "instrumentalness"]
    mood_avg = df.groupby("playlist_genre")[mood_cols].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    mood_avg.plot(kind="bar", ax=ax)
    ax.set_title("Mood Musik per Genre Playlist")
    st.pyplot(fig)

# 8. Mood Musik Radar Chart
elif option == "8. Mood Musik per Genre (Radar Chart)":
    import plotly.graph_objects as go

    st.header("📊 Mood Musik per Genre (Radar Chart)")
    mood_cols = ["valence", "energy", "acousticness", "danceability", "instrumentalness"]
    genres = df["playlist_genre"].unique()

    genre_choice = st.selectbox("Pilih Genre", genres)

    mood_vals = df[df["playlist_genre"] == genre_choice][mood_cols].mean()

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=mood_vals.values,
        theta=mood_cols,
        fill='toself',
        name=genre_choice
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title=f"Radar Chart Mood Musik: {genre_choice}"
    )
    st.plotly_chart(fig)

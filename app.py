import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from streamlit_lottie import st_lottie
import requests
from helpers.utils import (load_lottieurl, display_spotify_title, spotify_card, 
                           display_footer, load_and_prepare_data, display_metric)

# Konfigurasi halaman
st.set_page_config(
    page_title="Spotify Data Visualizer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menerapkan custom CSS
with open("style/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Lottie animation
lottie_music = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_w51pcehl.json")

# Load dan persiapkan data
df = load_and_prepare_data()

# Sidebar navigation
st.sidebar.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: #1DB954;'>🎵 Spotify Insights</h2></div>", unsafe_allow_html=True)

pages = {
    "🏠 Beranda": "home",
    "📊 Genre Analysis": "genre",
    "👨‍🎤 Artist Insights": "artist",
    "💃 Dance & Mood": "mood",
    "🎵 Audio Features": "audio",
    "📈 Playlist Analysis": "playlist"
}

# Sidebar navigation
selection = st.sidebar.radio("Navigasi", list(pages.keys()))

st.sidebar.markdown("---")
st.sidebar.info("""
**About This App**  
Aplikasi ini menyajikan visualisasi data dari dataset Spotify untuk memahami tren musik, preferensi pendengar, dan karakteristik audio.
""")

# Halaman Beranda
if selection == "🏠 Beranda":
    # Header section dengan animasi Lottie
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(lottie_music, height=300, key="music_home")
    with col2:
        st.markdown("""
        <h1 style='color: #1DB954; font-size: 3rem;'>Spotify Data Visualization</h1>
        <p style='font-size: 1.2rem; color: #B3B3B3;'>Explore music trends, genre popularities, and audio characteristics using Spotify data.</p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Highlights dan Metrik-metrik Penting
    st.header("📊 Dataset Highlights")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_songs = len(df)
        display_metric("Total Lagu", f"{total_songs:,}", icon="🎵")
    
    with col2:
        total_artists = df['track_artist'].nunique()
        display_metric("Jumlah Artis", f"{total_artists:,}", icon="👨‍🎤")
    
    with col3:
        avg_popularity = round(df['track_popularity'].mean(), 1)
        display_metric("Rata-rata Popularitas", avg_popularity, icon="⭐")
    
    with col4:
        genres = df['playlist_genre'].nunique()
        display_metric("Jumlah Genre", genres, icon="🎸")
    
    st.markdown("---")
    
    # Penjelasan tentang dataset
    st.header("🔍 Tentang Dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Dataset ini berisi lagu-lagu dari berbagai playlist Spotify, dengan fitur-fitur seperti:
        
        - **Track metadata**: Nama lagu, artis, album, tanggal rilis
        - **Audio features**: Danceability, energy, valence, acousticness, dll
        - **Playlist info**: Genre, subgenre
        - **Popularity**: Popularitas lagu (0-100)
        
        Data ini sangat berguna untuk memahami karakteristik musik dan tren di berbagai genre.
        """)
    
    with col2:
        st.image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png", width=250)
    
    st.markdown("---")
    
    # Highlight Cards - Temuan Menarik
    st.header("🔎 Highlights & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        spotify_card(
            "Genre Terpopuler",
            "Pop adalah genre dengan tingkat popularitas tertinggi, diikuti oleh Rap dan R&B.",
            "🏆"
        )
        
        spotify_card(
            "Tren Danceability",
            "Lagu-lagu EDM dan Pop memiliki danceability tertinggi, menunjukkan preferensi pendengar untuk musik yang bisa digunakan untuk menari.",
            "💃"
        )
    
    with col2:
        spotify_card(
            "Karakteristik Audio",
            "Lagu-lagu dengan energy dan loudness yang tinggi cenderung lebih populer di platform Spotify.",
            "🔊"
        )
        
        spotify_card(
            "Artis Teratas",
            "Artis dengan rata-rata popularitas tertinggi menunjukkan konsistensi dalam menghasilkan hit songs.",
            "🌟"
        )
    
    st.markdown("---")
    
    # Teaser visualisasi
    st.header("📈 Eksplorasi Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot sederhana untuk danceability vs energy
        fig = px.scatter(
            df.sample(1000), 
            x="danceability", 
            y="energy",
            color="playlist_genre",
            size="track_popularity",
            hover_name="track_name",
            title="Danceability vs Energy by Genre",
            labels={"danceability": "Danceability", "energy": "Energy", "playlist_genre": "Genre"},
            opacity=0.7
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar chart untuk rata-rata popularitas per genre
        genre_pop = df.groupby('playlist_genre')['track_popularity'].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=genre_pop.index, 
            y=genre_pop.values,
            color=genre_pop.values,
            color_continuous_scale='Viridis',
            title="Rata-rata Popularitas per Genre",
            labels={"x": "Genre", "y": "Popularitas", "color": "Popularitas"}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Call to action
    st.markdown("""
    <div style='background-color: #1DB954; padding: 1.5rem; border-radius: 10px; text-align: center; margin-top: 2rem;'>
        <h2 style='color: white; margin-bottom: 0.5rem;'>Jelajahi Lebih Lanjut!</h2>
        <p style='color: white;'>Gunakan menu navigasi di sidebar untuk menjelajahi analisis data yang lebih mendalam dan interaktif.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
display_footer()

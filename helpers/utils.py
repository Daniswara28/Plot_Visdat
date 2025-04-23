import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Fungsi untuk memuat animasi Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Fungsi untuk menampilkan judul dengan gaya Spotify
def display_spotify_title(title, icon="🎵"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
        <div style="font-size: 2.5rem; margin-right: 0.5rem;">{icon}</div>
        <h1 style="color: #1DB954; font-size: 2.5rem; font-weight: 700;">{title}</h1>
    </div>
    """, unsafe_allow_html=True)

# Fungsi untuk menampilkan metrik dengan gaya Spotify
def display_metric(label, value, delta=None, icon="📊"):
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"""
        <div style="font-size: 2rem; color: #1DB954; display: flex; align-items: center; justify-content: center; height: 100%;">
            {icon}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric(label=label, value=value, delta=delta)

# Fungsi untuk membuat card dengan gaya Spotify
def spotify_card(title, content, icon=None):
    icon_html = f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ""
    st.markdown(f"""
    <div style="background-color: #282828; border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem;">
        {icon_html}
        <h3 style="color: #1DB954; margin-bottom: 0.8rem;">{title}</h3>
        <div style="color: #FFFFFF;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# Fungsi untuk menampilkan footer
def display_footer():
    st.markdown("""
    <div class="footer">
        <p>Analisis Data Spotify &copy; 2024 | Dibuat dengan ❤️ dan Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# Fungsi untuk mempersiapkan data
def load_and_prepare_data():
    df = pd.read_csv("spotify_songs.csv")
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
    df['year'] = df['track_album_release_date'].dt.year
    return df

# Plot Genres Favorit
def plot_favorite_genres(df, year=2020):
    df_year = df[df['year'] == year]
    genre_popularity = df_year.groupby('playlist_genre')['track_popularity'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=genre_popularity.values, 
        y=genre_popularity.index,
        orientation='h',
        color=genre_popularity.values,
        color_continuous_scale='Viridis',
        title=f"Popularitas Genre Musik Tahun {year}",
        labels={'x': 'Popularitas', 'y': 'Genre', 'color': 'Popularitas'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        coloraxis_colorbar=dict(title='Popularitas'),
        height=500
    )
    
    return fig

# Plot Top Artists
def plot_top_artists(df, n=10):
    top_artist = df.groupby('track_artist')['track_popularity'].mean().sort_values(ascending=False).head(n)
    
    fig = px.bar(
        x=top_artist.values, 
        y=top_artist.index,
        orientation='h',
        color=top_artist.values,
        color_continuous_scale='Viridis',
        title=f"Top {n} Artis Berdasarkan Popularitas",
        labels={'x': 'Popularitas', 'y': 'Artis', 'color': 'Popularitas'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600
    )
    
    return fig

# Plot Music Trends
def plot_music_trends(df, min_year=2010):
    trend = df[df['year'] >= min_year].groupby(['year', 'playlist_genre'])['track_popularity'].mean().reset_index()
    
    fig = px.line(
        trend, 
        x='year', 
        y='track_popularity', 
        color='playlist_genre',
        markers=True,
        title='Perubahan Popularitas Genre Musik dari Tahun ke Tahun',
        labels={'track_popularity': 'Popularitas', 'year': 'Tahun', 'playlist_genre': 'Genre'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig

# Mood Radar Chart
def plot_mood_radar(df, genre):
    mood_cols = ["valence", "energy", "acousticness", "danceability", "instrumentalness"]
    mood_vals = df[df["playlist_genre"] == genre][mood_cols].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=mood_vals.values,
        theta=mood_cols,
        fill='toself',
        name=genre,
        line=dict(color='#1DB954')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),
            bgcolor='rgba(40,40,40,0.8)'
        ),
        showlegend=False,
        title=f"Radar Chart Mood Musik: {genre}",
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white'
    )
    
    return fig 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helpers.utils import (display_spotify_title, spotify_card, display_footer,
                          load_and_prepare_data, plot_top_artists)

# Konfigurasi halaman
st.set_page_config(
    page_title="Artist Insights | Spotify Data",
    page_icon="👨‍🎤",
    layout="wide"
)

# Menerapkan custom CSS
with open("style/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
df = load_and_prepare_data()

# Header
display_spotify_title("Analisis Artis", "👨‍🎤")

st.markdown("""
<p style="font-size: 1.2rem; color: #B3B3B3; margin-bottom: 2rem; text-align: center;">
    Jelajahi artis-artis paling populer dan karakteristik musik mereka
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Tabs untuk berbagai analisis
tab1, tab2, tab3 = st.tabs(["🏆 Top Artis", "🎸 Gaya Musik Artis", "🌟 Konsistensi Artis"])

# Tab 1: Top Artis
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Artis Paling Populer")
        
        # Pilih jumlah artis
        top_n = st.slider("Jumlah Artis", 5, 20, 10)
        
        # Filter genre
        genres = ["Semua Genre"] + sorted(df['playlist_genre'].unique().tolist())
        selected_genre = st.selectbox("Filter Genre", genres)
        
        # Informasi tambahan
        spotify_card(
            "Apa itu Popularitas Artis?",
            "Popularitas artis dihitung berdasarkan rata-rata popularitas semua lagu artis tersebut dalam dataset. Hal ini mencerminkan seberapa disukai artis tersebut di Spotify.",
            "💡"
        )
    
    with col2:
        # Filter data berdasarkan genre jika dipilih
        if selected_genre != "Semua Genre":
            genre_df = df[df['playlist_genre'] == selected_genre]
        else:
            genre_df = df
        
        # Plot top artists
        fig = plot_top_artists(genre_df, top_n)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis tambahan - Distribusi popularitas
    st.subheader("Distribusi Popularitas Artis")
    
    # Hitung jumlah lagu dan rata-rata popularitas per artis
    artist_stats = df.groupby('track_artist').agg({
        'track_popularity': ['mean', 'count']
    }).reset_index()
    
    artist_stats.columns = ['artist', 'avg_popularity', 'song_count']
    
    # Plot scatter antara jumlah lagu dan popularitas
    fig = px.scatter(
        artist_stats[artist_stats['song_count'] >= 3],
        x="song_count",
        y="avg_popularity",
        size="song_count",
        color="avg_popularity",
        color_continuous_scale='Viridis',
        hover_name="artist",
        log_x=True,
        title="Hubungan antara Jumlah Lagu dan Popularitas Artis",
        labels={
            "song_count": "Jumlah Lagu (log scale)",
            "avg_popularity": "Rata-rata Popularitas",
            "artist": "Artis"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan scatter plot
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Penjelasan Scatter Plot</h4>
        <p style="color: #FFFFFF;">
            Graf di atas menunjukkan hubungan antara jumlah lagu dan popularitas artis. Beberapa insight:
            <ul>
                <li>Artis dengan lebih banyak lagu tidak selalu lebih populer</li>
                <li>Beberapa artis dengan sedikit lagu bisa sangat populer (bintang baru atau one-hit wonders)</li>
                <li>Ukuran lingkaran menunjukkan jumlah lagu, sementara warna menunjukkan tingkat popularitas</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Gaya Musik Artis
with tab2:
    st.subheader("Karakteristik Musik dari Artis Populer")
    
    # Pilih artis untuk dianalisis
    top_artists = df.groupby('track_artist')['track_popularity'].mean().sort_values(ascending=False).head(50)
    selected_artists = st.multiselect("Pilih Artis untuk Dibandingkan", top_artists.index.tolist(), default=top_artists.index.tolist()[:3])
    
    if selected_artists:
        # Pilih fitur audio untuk dibandingkan
        audio_features = ["danceability", "energy", "acousticness", "valence", "speechiness", "instrumentalness", "liveness"]
        
        # Hitung rata-rata fitur audio untuk setiap artis
        artist_features = df[df['track_artist'].isin(selected_artists)].groupby('track_artist')[audio_features].mean()
        
        # Tampilkan data dalam bentuk radar chart
        fig = go.Figure()
        
        for artist in artist_features.index:
            fig.add_trace(go.Scatterpolar(
                r=artist_features.loc[artist, :].values,
                theta=audio_features,
                fill='toself',
                name=artist
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                ),
                bgcolor='rgba(40,40,40,0.8)'
            ),
            title="Karakteristik Audio dari Artis Terpilih",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Penjelasan radar chart
        st.markdown("""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
            <h4 style="color: #1DB954;">Memahami Radar Chart</h4>
            <p style="color: #FFFFFF;">
                Radar chart di atas memungkinkan Anda membandingkan gaya musik dari beberapa artis berdasarkan karakteristik audio mereka:
                <ul>
                    <li><strong>Danceability</strong>: Seberapa cocok untuk menari (0-1)</li>
                    <li><strong>Energy</strong>: Intensitas dan aktivitas (0-1)</li>
                    <li><strong>Acousticness</strong>: Tingkat akustik (0-1)</li>
                    <li><strong>Valence</strong>: Positivitas musik (0=sedih, 1=senang)</li>
                    <li><strong>Speechiness</strong>: Keberadaan kata-kata yang diucapkan (0-1)</li>
                    <li><strong>Instrumentalness</strong>: Ketiadaan vokal (0-1)</li>
                    <li><strong>Liveness</strong>: Keberadaan penonton (0-1)</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pilih setidaknya satu artis untuk melihat profil musiknya")

# Tab 3: Konsistensi Artis
with tab3:
    st.subheader("Konsistensi Popularitas Artis")
    
    # Pilih artis untuk dianalisis
    top_artists = df.groupby('track_artist')['track_popularity'].count().sort_values(ascending=False).head(30)
    top_artists = top_artists[top_artists >= 5]  # Artis dengan minimal 5 lagu
    selected_artist = st.selectbox("Pilih Artis", top_artists.index.tolist())
    
    if selected_artist:
        # Dapatkan semua lagu dari artis tersebut
        artist_songs = df[df['track_artist'] == selected_artist].sort_values('track_popularity', ascending=False)
        
        # Distribusi popularitas lagu
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Rata-rata popularitas
            avg_pop = artist_songs['track_popularity'].mean()
            std_pop = artist_songs['track_popularity'].std()
            
            # Visualisasi ringkasan statistik
            st.markdown(f"""
            <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                <h4 style="color: #1DB954;">Ringkasan Popularitas</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem;">
                    <strong>Rata-rata:</strong> {avg_pop:.1f} / 100<br>
                    <strong>Std Deviasi:</strong> {std_pop:.1f}<br>
                    <strong>Jumlah Lagu:</strong> {len(artist_songs)}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Kalkulasi Indeks Konsistensi (semakin rendah standar deviasi, semakin konsisten)
            consistency_index = 100 - min(std_pop * 5, 100)  # Skala 0-100
            
            # Tampilkan gauge chart untuk konsistensi
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = consistency_index,
                title = {'text': "Indeks Konsistensi"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1DB954"},
                    'steps': [
                        {'range': [0, 40], 'color': "#E51D2A"},
                        {'range': [40, 70], 'color': "#FFC83D"},
                        {'range': [70, 100], 'color': "#1DB954"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': consistency_index
                    }
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(40,40,40,0.8)',
                font_color='white',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Penjelasan Indeks Konsistensi
            st.markdown("""
            <div style="background-color: #282828; padding: 1rem; border-radius: 10px; margin-top: 1rem; font-size: 0.9rem;">
                <p style="color: #FFFFFF;">
                    <strong>Indeks Konsistensi</strong> mengukur seberapa konsisten popularitas lagu-lagu artis.
                    Semakin tinggi nilai (mendekati 100), semakin konsisten artis tersebut
                    dalam menghasilkan lagu-lagu dengan tingkat popularitas yang serupa.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Plot horizontal bar chart untuk semua lagu
            fig = px.bar(
                artist_songs.head(15),
                y='track_name',
                x='track_popularity',
                orientation='h',
                color='track_popularity',
                color_continuous_scale='Viridis',
                title=f"Top 15 Lagu Populer dari {selected_artist}",
                labels={
                    'track_popularity': 'Popularitas',
                    'track_name': 'Judul Lagu'
                }
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(40,40,40,0.8)',
                paper_bgcolor='rgba(40,40,40,0.8)',
                font_color='white',
                height=500,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Histogram popularitas
        fig = px.histogram(
            artist_songs,
            x='track_popularity',
            color_discrete_sequence=['#1DB954'],
            nbins=20,
            title=f"Distribusi Popularitas Lagu {selected_artist}",
            labels={'track_popularity': 'Popularitas'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tampilkan tabel lagu
        st.subheader(f"Daftar Lagu dari {selected_artist}")
        
        # Tampilkan tabel dengan styling
        st.dataframe(
            artist_songs[['track_name', 'track_popularity', 'playlist_genre', 'playlist_subgenre']].reset_index(drop=True),
            use_container_width=True,
            column_config={
                "track_name": "Judul Lagu",
                "track_popularity": st.column_config.ProgressColumn(
                    "Popularitas",
                    format="%d",
                    min_value=0,
                    max_value=100
                ),
                "playlist_genre": "Genre",
                "playlist_subgenre": "Subgenre"
            }
        )

# Footer
display_footer() 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from helpers.utils import (display_spotify_title, spotify_card, display_footer,
                          load_and_prepare_data, plot_mood_radar)

# Konfigurasi halaman
st.set_page_config(
    page_title="Playlist Analysis | Spotify Data",
    page_icon="📊",
    layout="wide"
)

# Menerapkan custom CSS
with open("style/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
df = load_and_prepare_data()

# Header
display_spotify_title("Analisis Playlist", "📊")

st.markdown("""
<p style="font-size: 1.2rem; color: #B3B3B3; margin-bottom: 2rem; text-align: center;">
    Jelajahi karakteristik dan pola di berbagai playlist Spotify
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Tabs untuk berbagai analisis
tab1, tab2, tab3 = st.tabs(["📋 Overview Playlist", "🎯 Perbandingan Playlist", "🧩 Subgenre Analysis"])

# Tab 1: Overview Playlist
with tab1:
    st.subheader("Overview Playlist")
    
    # Ringkasan statistik playlist
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Jumlah lagu per genre
        genre_counts = df['playlist_genre'].value_counts().reset_index()
        genre_counts.columns = ['genre', 'count']
        
        fig = px.pie(
            genre_counts,
            values='count',
            names='genre',
            title="Distribusi Lagu per Genre Playlist",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Jumlah playlist per genre
        playlist_counts = df.groupby('playlist_genre')['playlist_id'].nunique().reset_index()
        playlist_counts.columns = ['genre', 'count']
        
        fig = px.bar(
            playlist_counts,
            x='genre',
            y='count',
            color='genre',
            title="Jumlah Playlist per Genre",
            labels={'count': 'Jumlah Playlist', 'genre': 'Genre'}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Informasi tentang playlist
    st.subheader("Informasi Playlist")
    
    # Statistik playlist
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_playlists = df['playlist_id'].nunique()
        st.markdown(f"""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; color: #1DB954; margin-bottom: 0.5rem;">{total_playlists}</div>
            <div style="color: #FFFFFF; font-size: 1.2rem;">Total Playlist</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_songs = int(df.groupby('playlist_id')['track_id'].count().mean())
        st.markdown(f"""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; color: #1DB954; margin-bottom: 0.5rem;">{avg_songs}</div>
            <div style="color: #FFFFFF; font-size: 1.2rem;">Rata-rata Lagu per Playlist</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_subgenres = df['playlist_subgenre'].nunique()
        st.markdown(f"""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; color: #1DB954; margin-bottom: 0.5rem;">{total_subgenres}</div>
            <div style="color: #FFFFFF; font-size: 1.2rem;">Total Subgenre</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistik lagu per playlist berdasarkan genre
    st.subheader("Lagu per Playlist berdasarkan Genre")
    
    songs_per_playlist = df.groupby(['playlist_genre', 'playlist_id'])['track_id'].count().reset_index()
    songs_per_playlist.columns = ['genre', 'playlist_id', 'song_count']
    
    fig = px.box(
        songs_per_playlist,
        x='genre',
        y='song_count',
        color='genre',
        title="Distribusi Jumlah Lagu per Playlist",
        labels={'song_count': 'Jumlah Lagu', 'genre': 'Genre'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight tentang playlist
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Insight tentang Playlist</h4>
        <p style="color: #FFFFFF;">
            Dari visualisasi di atas, kita dapat mengamati:
            <ul>
                <li>Distribusi lagu tidak merata di berbagai genre - beberapa genre lebih dominan dalam dataset</li>
                <li>Playlist EDM cenderung memiliki lebih banyak lagu dibandingkan genre lain</li>
                <li>Ada variasi yang signifikan dalam jumlah lagu per playlist di beberapa genre</li>
                <li>Playlist musik rock menunjukkan konsistensi dalam jumlah lagu (varians rendah)</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Perbandingan Playlist
with tab2:
    st.subheader("Perbandingan Karakteristik Playlist")
    
    # Pilih playlist untuk dibandingkan
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Filter genre
        genres = sorted(df['playlist_genre'].unique())
        selected_genres = st.multiselect("Pilih Genre", genres, default=genres[:2])
        
        # Pilih fitur audio untuk dibandingkan
        audio_features = ["danceability", "energy", "acousticness", "valence", "speechiness", "instrumentalness", "liveness"]
        selected_features = st.multiselect("Pilih Fitur Audio", audio_features, default=audio_features)
        
        # Informasi tentang perbandingan
        spotify_card(
            "Cara Membaca Radar Chart",
            "Radar chart memungkinkan perbandingan beberapa dimensi fitur audio secara bersamaan. Semakin jauh dari pusat, semakin tinggi nilai fitur tersebut.",
            "📊"
        )
    
    with col2:
        if selected_genres and selected_features:
            # Hitung rata-rata fitur audio untuk setiap genre
            genre_features = df[df['playlist_genre'].isin(selected_genres)].groupby('playlist_genre')[selected_features].mean()
            
            # Tampilkan data dalam bentuk radar chart
            fig = go.Figure()
            
            for genre in genre_features.index:
                fig.add_trace(go.Scatterpolar(
                    r=genre_features.loc[genre, :].values,
                    theta=selected_features,
                    fill='toself',
                    name=genre
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    ),
                    bgcolor='rgba(40,40,40,0.8)'
                ),
                title="Perbandingan Karakteristik Audio antar Genre Playlist",
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
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Pilih setidaknya satu genre dan satu fitur audio untuk melihat perbandingan")
    
    # Perbandingan popularitas playlist
    st.subheader("Perbandingan Popularitas antar Playlist")
    
    # Hitung rata-rata popularitas per genre dan subgenre
    popularity_by_subgenre = df.groupby(['playlist_genre', 'playlist_subgenre'])['track_popularity'].mean().reset_index()
    
    # Plot popularitas
    fig = px.treemap(
        popularity_by_subgenre,
        path=[px.Constant("Semua Genre"), 'playlist_genre', 'playlist_subgenre'],
        values='track_popularity',
        color='track_popularity',
        color_continuous_scale='Viridis',
        title="Popularitas Playlist berdasarkan Genre dan Subgenre",
        labels={'track_popularity': 'Popularitas Rata-rata'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan treemap
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Memahami Treemap</h4>
        <p style="color: #FFFFFF;">
            Treemap di atas visualisasikan struktur genre dan subgenre:
            <ul>
                <li>Ukuran kotak menunjukkan nilai popularitas relatif</li>
                <li>Warna menunjukkan tingkat popularitas (semakin cerah = semakin populer)</li>
                <li>Struktur hierarkis memungkinkan analisis dari genre hingga subgenre</li>
                <li>Klik pada genre untuk memperbesar dan melihat detail subgenre</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analisis similarities antar playlist
    st.subheader("Kemiripan antar Playlist Genre")
    
    # Hitung rata-rata fitur audio untuk setiap genre
    genre_feat_avg = df.groupby('playlist_genre')[audio_features].mean()
    
    # Buat matriks jarak (disimilarity) menggunakan korelasi
    from scipy.spatial.distance import pdist, squareform
    
    # Hitung jarak euclidean antar genre
    dist_matrix = pd.DataFrame(
        squareform(pdist(genre_feat_avg.values, 'euclidean')),
        columns=genre_feat_avg.index,
        index=genre_feat_avg.index
    )
    
    # Konversi ke similarity (semakin dekat ke 1, semakin mirip)
    max_dist = dist_matrix.max().max()
    similarity_matrix = 1 - (dist_matrix / max_dist)
    
    # Plot heatmap
    fig = px.imshow(
        similarity_matrix,
        text_auto='.2f',
        color_continuous_scale='Viridis',
        title="Matriks Kemiripan antar Genre Playlist",
        labels=dict(x="Genre", y="Genre", color="Similarity")
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan matriks kemiripan
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Memahami Matriks Kemiripan</h4>
        <p style="color: #FFFFFF;">
            Matriks kemiripan menunjukkan seberapa mirip karakteristik audio antar genre playlist:
            <ul>
                <li>Nilai mendekati 1.0 (lebih cerah) menunjukkan kemiripan yang tinggi</li>
                <li>Nilai mendekati 0.0 (lebih gelap) menunjukkan perbedaan yang besar</li>
                <li>Diagonal utama selalu 1.0 karena genre identik dengan dirinya sendiri</li>
                <li>Kemiripan tinggi mengindikasikan karakteristik audio yang serupa antar genre</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 3: Subgenre Analysis
with tab3:
    st.subheader("Analisis Subgenre")
    
    # Pilih genre untuk analisis subgenre
    genre_for_subgenre = st.selectbox("Pilih Genre", sorted(df['playlist_genre'].unique()))
    
    if genre_for_subgenre:
        # Filter data untuk genre yang dipilih
        genre_df = df[df['playlist_genre'] == genre_for_subgenre]
        
        # Hitung jumlah lagu per subgenre
        subgenre_counts = genre_df['playlist_subgenre'].value_counts()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Pie chart untuk distribusi subgenre
            fig = px.pie(
                values=subgenre_counts.values,
                names=subgenre_counts.index,
                title=f"Distribusi Subgenre dalam {genre_for_subgenre}",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(40,40,40,0.8)',
                paper_bgcolor='rgba(40,40,40,0.8)',
                font_color='white',
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Popularitas per subgenre
            subgenre_popularity = genre_df.groupby('playlist_subgenre')['track_popularity'].mean().sort_values(ascending=False)
            
            fig = px.bar(
                x=subgenre_popularity.index,
                y=subgenre_popularity.values,
                color=subgenre_popularity.values,
                color_continuous_scale='Viridis',
                title=f"Popularitas Subgenre dalam {genre_for_subgenre}",
                labels={'x': 'Subgenre', 'y': 'Popularitas', 'color': 'Popularitas'}
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(40,40,40,0.8)',
                paper_bgcolor='rgba(40,40,40,0.8)',
                font_color='white',
                xaxis={'tickangle': 45},
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Radar chart untuk subgenre
        st.subheader(f"Karakteristik Audio Subgenre dalam {genre_for_subgenre}")
        
        # Pilih subgenre untuk perbandingan
        subgenres = sorted(genre_df['playlist_subgenre'].unique())
        selected_subgenres = st.multiselect("Pilih Subgenre untuk Dibandingkan", subgenres, default=subgenres[:min(3, len(subgenres))])
        
        if selected_subgenres:
            # Fitur audio untuk perbandingan
            audio_features = ["danceability", "energy", "acousticness", "valence", "speechiness", "instrumentalness", "liveness"]
            
            # Hitung rata-rata fitur audio untuk setiap subgenre
            subgenre_features = genre_df[genre_df['playlist_subgenre'].isin(selected_subgenres)].groupby('playlist_subgenre')[audio_features].mean()
            
            # Tampilkan radar chart
            fig = go.Figure()
            
            for subgenre in subgenre_features.index:
                fig.add_trace(go.Scatterpolar(
                    r=subgenre_features.loc[subgenre, :].values,
                    theta=audio_features,
                    fill='toself',
                    name=subgenre
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    ),
                    bgcolor='rgba(40,40,40,0.8)'
                ),
                title=f"Perbandingan Karakteristik Audio antar Subgenre {genre_for_subgenre}",
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
        
        # Top artis per subgenre
        st.subheader(f"Top Artis per Subgenre dalam {genre_for_subgenre}")
        
        # Pilih subgenre
        selected_subgenre = st.selectbox("Pilih Subgenre", subgenres)
        
        if selected_subgenre:
            # Filter data untuk subgenre yang dipilih
            subgenre_df = genre_df[genre_df['playlist_subgenre'] == selected_subgenre]
            
            # Hitung rata-rata popularitas per artis
            artist_popularity = subgenre_df.groupby('track_artist')['track_popularity'].mean().sort_values(ascending=False).head(10)
            
            # Plot top artis
            fig = px.bar(
                x=artist_popularity.values,
                y=artist_popularity.index,
                orientation='h',
                color=artist_popularity.values,
                color_continuous_scale='Viridis',
                title=f"Top 10 Artis di Subgenre {selected_subgenre}",
                labels={'x': 'Popularitas', 'y': 'Artis', 'color': 'Popularitas'}
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(40,40,40,0.8)',
                paper_bgcolor='rgba(40,40,40,0.8)',
                font_color='white',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Penjelasan top artis
            st.markdown(f"""
            <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
                <h4 style="color: #1DB954;">Top Artis di {selected_subgenre}</h4>
                <p style="color: #FFFFFF;">
                    Graf di atas menunjukkan artis paling populer di subgenre {selected_subgenre}. Artis ini:
                    <ul>
                        <li>Memiliki rata-rata popularitas lagu tertinggi dalam subgenre ini</li>
                        <li>Mungkin menjadi pengaruh utama dalam bentuk dan arah subgenre</li>
                        <li>Sering dimasukkan ke dalam playlist {selected_subgenre}</li>
                        <li>Mungkin mewakili "sound" khas dari subgenre ini</li>
                    </ul>
                </p>
            </div>
            """, unsafe_allow_html=True)

# Footer
display_footer() 
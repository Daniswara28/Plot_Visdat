import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helpers.utils import (display_spotify_title, spotify_card, display_footer,
                          load_and_prepare_data, plot_favorite_genres, plot_music_trends)

# Konfigurasi halaman
st.set_page_config(
    page_title="Genre Analysis | Spotify Data",
    page_icon="🎵",
    layout="wide"
)

# Menerapkan custom CSS
with open("style/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
df = load_and_prepare_data()

# Header
display_spotify_title("Analisis Genre Musik", "🎸")

st.markdown("""
<p style="font-size: 1.2rem; color: #B3B3B3; margin-bottom: 2rem; text-align: center;">
    Jelajahi tren, popularitas, dan karakteristik berbagai genre musik di Spotify
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Tabs untuk berbagai analisis
tab1, tab2, tab3 = st.tabs(["📊 Popularitas Genre", "📈 Tren Genre", "🎵 Karakteristik Genre"])

# Tab 1: Popularitas Genre
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Genre Musik Paling Populer")
        
        # Filter tahun
        years = sorted(df['year'].dropna().unique())
        selected_year = st.selectbox("Pilih Tahun", years, index=len(years)-1)
        
        # Informasi tambahan
        st.markdown("""
        **Apa itu Popularitas?**
        
        Skor popularitas (0-100) menunjukkan seberapa populer lagu tersebut, berdasarkan:
        - Jumlah streaming
        - Banyaknya simpan ke pustaka
        - Shared di media sosial
        - Dan metrik lainnya
        """)
        
        # Menambahkan card info
        spotify_card(
            "Tahukah Kamu?",
            "Popularitas genre dapat berubah signifikan dari tahun ke tahun, dipengaruhi oleh tren, artis baru, dan perubahan selera pendengar.",
            "💡"
        )
    
    with col2:
        # Plot genre popularity
        fig = plot_favorite_genres(df, selected_year)
        st.plotly_chart(fig, use_container_width=True)
    
    # Analisis tambahan
    st.subheader("Subgenre Terpopuler")
    
    # Filter genre
    genres = sorted(df['playlist_genre'].unique())
    selected_genre = st.selectbox("Pilih Genre", genres)
    
    # Filter data
    filtered_df = df[df['playlist_genre'] == selected_genre]
    
    # Plot subgenre popularity
    subgenre_pop = filtered_df.groupby('playlist_subgenre')['track_popularity'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=subgenre_pop.index, 
        y=subgenre_pop.values,
        color=subgenre_pop.values,
        color_continuous_scale='Viridis',
        title=f"Popularitas Subgenre dalam {selected_genre}",
        labels={"x": "Subgenre", "y": "Popularitas", "color": "Popularitas"}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Tren Genre
with tab2:
    st.subheader("Tren Popularitas Genre dari Tahun ke Tahun")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Filter tahun
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        year_range = st.slider("Rentang Tahun", min_year, max_year, (2010, max_year))
        
        # Pilih genre untuk highlight
        genres = sorted(df['playlist_genre'].unique())
        highlight_genre = st.multiselect("Highlight Genre", genres, default=["pop", "rap"])
        
        # Info card
        spotify_card(
            "Analisis Tren",
            "Perhatikan bagaimana popularitas genre berubah dari waktu ke waktu. Perubahan ini mencerminkan pergeseran minat pendengar dan perkembangan industri musik.",
            "📊"
        )
    
    with col2:
        # Filter berdasarkan rentang tahun
        trend_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
        
        # Prepare data
        trend = trend_df.groupby(['year', 'playlist_genre'])['track_popularity'].mean().reset_index()
        
        # Highlight selected genres
        if highlight_genre:
            trend['highlight'] = trend['playlist_genre'].apply(lambda x: "Highlight" if x in highlight_genre else "Background")
            
            fig = px.line(
                trend, 
                x='year', 
                y='track_popularity', 
                color='playlist_genre',
                line_dash='highlight',
                color_discrete_sequence=px.colors.qualitative.Vivid,
                markers=True,
                title='Perubahan Popularitas Genre Musik dari Tahun ke Tahun',
                labels={'track_popularity': 'Popularitas', 'year': 'Tahun', 'playlist_genre': 'Genre'}
            )
            
            # Membuat genre yang di-highlight lebih tebal
            for i, genre in enumerate(trend['playlist_genre'].unique()):
                if genre in highlight_genre:
                    fig.data[i].line.width = 4
                else:
                    fig.data[i].line.width = 1.5
                    fig.data[i].opacity = 0.5
        else:
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
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tambahan analisis perubahan peringkat
    st.subheader("Perubahan Peringkat Genre")
    
    # Tahun awal dan akhir untuk perbandingan
    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox("Tahun Awal", sorted(df['year'].dropna().unique()), index=5)
    with col2:
        end_year = st.selectbox("Tahun Akhir", sorted(df['year'].dropna().unique()), index=-1)
    
    # Hitung peringkat untuk kedua tahun
    start_rank = df[df['year'] == start_year].groupby('playlist_genre')['track_popularity'].mean().sort_values(ascending=False)
    end_rank = df[df['year'] == end_year].groupby('playlist_genre')['track_popularity'].mean().sort_values(ascending=False)
    
    # Konversi ke peringkat
    start_rank = start_rank.reset_index()
    start_rank['rank'] = range(1, len(start_rank) + 1)
    start_rank = start_rank.set_index('playlist_genre')
    
    end_rank = end_rank.reset_index()
    end_rank['rank'] = range(1, len(end_rank) + 1)
    end_rank = end_rank.set_index('playlist_genre')
    
    # Gabungkan kedua dataframe
    rank_change = pd.DataFrame({
        'genre': start_rank.index,
        'rank_start': start_rank['rank'],
        'rank_end': [end_rank.loc[genre, 'rank'] if genre in end_rank.index else None for genre in start_rank.index]
    }).dropna()
    
    # Hitung perubahan peringkat
    rank_change['change'] = rank_change['rank_start'] - rank_change['rank_end']
    rank_change['abs_change'] = abs(rank_change['change'])
    rank_change['direction'] = rank_change['change'].apply(lambda x: "Naik" if x > 0 else "Turun" if x < 0 else "Tetap")
    rank_change['color'] = rank_change['change'].apply(lambda x: "#1DB954" if x > 0 else "#E51D2A" if x < 0 else "#B3B3B3")
    
    # Urutkan berdasarkan perubahan absolut
    rank_change = rank_change.sort_values('abs_change', ascending=False).head(10)
    
    # Plot perubahan peringkat
    fig = go.Figure()
    
    for i, row in rank_change.iterrows():
        fig.add_trace(go.Scatter(
            x=[start_year, end_year],
            y=[row['rank_start'], row['rank_end']],
            mode='lines+markers+text',
            name=row['genre'],
            line=dict(width=2, color=row['color']),
            marker=dict(size=10),
            text=[f"{int(row['rank_start'])}", f"{int(row['rank_end'])}"],
            textposition="top center"
        ))
    
    # Invert y-axis so that rank 1 is at the top
    fig.update_layout(
        title=f"Perubahan Peringkat Genre dari {start_year} ke {end_year}",
        xaxis_title="Tahun",
        yaxis_title="Peringkat",
        yaxis=dict(autorange="reversed"),  # Memastikan peringkat 1 di atas
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Karakteristik Genre
with tab3:
    st.subheader("Karakteristik Audio per Genre")
    
    # Pilih karakteristik audio
    audio_features = ["danceability", "energy", "acousticness", "instrumentalness", "valence", "speechiness", "liveness"]
    x_feature = st.selectbox("Pilih Karakteristik X", audio_features, index=0)
    y_feature = st.selectbox("Pilih Karakteristik Y", audio_features, index=1)
    
    # Plot bubble chart untuk perbandingan karakteristik antar genre
    genre_features = df.groupby('playlist_genre')[audio_features + ['track_popularity']].mean().reset_index()
    
    fig = px.scatter(
        genre_features,
        x=x_feature,
        y=y_feature,
        size="track_popularity",
        color="playlist_genre",
        hover_name="playlist_genre",
        size_max=40,
        title=f"Perbandingan {x_feature.capitalize()} vs {y_feature.capitalize()} antar Genre"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600,
        xaxis=dict(title=x_feature.capitalize()),
        yaxis=dict(title=y_feature.capitalize())
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan fitur audio
    col1, col2 = st.columns(2)
    
    with col1:
        spotify_card(
            "Danceability",
            "Menggambarkan seberapa cocok lagu untuk menari berdasarkan kombinasi elemen musik seperti tempo, stabilitas ritme, kekuatan beat, dan keteraturan secara keseluruhan. Nilai 0.0 paling tidak bisa digunakan untuk menari dan 1.0 paling bisa digunakan untuk menari.",
            "💃"
        )
        
        spotify_card(
            "Energy",
            "Ukuran dari 0.0 hingga 1.0 yang mewakili ukuran persepsi tentang intensitas dan aktivitas. Biasanya, lagu yang energik terasa cepat, keras, dan bising.",
            "⚡"
        )
        
        spotify_card(
            "Valence",
            "Ukuran dari 0.0 hingga 1.0 yang menggambarkan positivitas musik yang disampaikan oleh sebuah lagu. Lagu dengan valence tinggi terdengar lebih positif (mis. senang, ceria, euforia), sementara lagu dengan valence rendah terdengar lebih negatif (mis. sedih, depresi, marah).",
            "😊"
        )
    
    with col2:
        spotify_card(
            "Acousticness",
            "Ukuran kepercayaan dari 0.0 hingga 1.0 apakah lagu tersebut akustik. 1.0 mewakili kepercayaan tinggi bahwa lagu tersebut akustik.",
            "🎻"
        )
        
        spotify_card(
            "Instrumentalness",
            "Memprediksi apakah sebuah lagu tidak mengandung vokal. Suara 'Ooh' dan 'aah' diperlakukan sebagai instrumental dalam konteks ini. Semakin dekat nilai instrumentalness ke 1.0, semakin besar kemungkinan lagu tersebut tidak mengandung konten vokal.",
            "🎹"
        )
        
        spotify_card(
            "Speechiness",
            "Speechiness mendeteksi keberadaan kata-kata yang diucapkan dalam sebuah lagu. Semakin eksklusif lagu tersebut seperti pembicaraan (mis. talk show, audio book, puisi), semakin dekat nilai atribut ke 1.0.",
            "🗣️"
        )

# Footer
display_footer() 
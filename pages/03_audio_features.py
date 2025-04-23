import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from helpers.utils import (display_spotify_title, spotify_card, display_footer,
                          load_and_prepare_data)

# Konfigurasi halaman
st.set_page_config(
    page_title="Audio Features | Spotify Data",
    page_icon="🎵",
    layout="wide"
)

# Menerapkan custom CSS
with open("style/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
df = load_and_prepare_data()

# Header
display_spotify_title("Analisis Fitur Audio", "🎚️")

st.markdown("""
<p style="font-size: 1.2rem; color: #B3B3B3; margin-bottom: 2rem; text-align: center;">
    Jelajahi karakteristik dan fitur audio dari lagu-lagu Spotify seperti danceability, energy, valence, dan lainnya
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Tabs untuk berbagai analisis
tab1, tab2, tab3, tab4 = st.tabs(["💃 Danceability", "⚡ Energy", "😊 Valence", "🔍 Tempo & Duration"])

# Tab 1: Danceability
with tab1:
    st.subheader("Analisis Danceability")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #1DB954;">Apa itu Danceability?</h4>
            <p style="color: #FFFFFF;">
                Danceability menggambarkan seberapa cocok lagu untuk menari berdasarkan kombinasi elemen musik seperti tempo, 
                stabilitas ritme, kekuatan beat, dan keteraturan secara keseluruhan.
                <br><br>
                <strong>Skala:</strong> 0.0 (paling tidak cocok untuk menari) sampai 1.0 (paling cocok untuk menari)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter genre
        genres = ["Semua Genre"] + sorted(df['playlist_genre'].unique().tolist())
        selected_genre = st.selectbox("Filter Genre", genres, key="dance_genre")
        
        # Tambahkan informasi tambahan
        spotify_card(
            "Tahukah Kamu?",
            "Lagu-lagu dengan danceability tinggi cenderung memiliki ritme yang stabil, beat yang kuat, dan tempo yang konsisten.",
            "💡"
        )
    
    with col2:
        # Filter data berdasarkan genre
        if selected_genre != "Semua Genre":
            genre_df = df[df['playlist_genre'] == selected_genre]
        else:
            genre_df = df
        
        # Histogram danceability
        fig = px.histogram(
            genre_df,
            x="danceability",
            color="playlist_genre" if selected_genre == "Semua Genre" else None,
            nbins=30,
            opacity=0.7,
            title="Distribusi Danceability" + (f" - {selected_genre}" if selected_genre != "Semua Genre" else ""),
            labels={"danceability": "Danceability", "count": "Jumlah Lagu"}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Rata-rata danceability per genre
    st.subheader("Perbandingan Danceability antar Genre")
    
    # Menghitung rata-rata danceability per genre
    dance_avg = df.groupby('playlist_genre')['danceability'].mean().sort_values(ascending=False)
    dance_std = df.groupby('playlist_genre')['danceability'].std()
    
    # Membuat dataframe untuk plotting
    dance_stats = pd.DataFrame({
        'genre': dance_avg.index,
        'avg_danceability': dance_avg.values,
        'std_danceability': dance_std.values
    })
    
    # Plot bar chart dengan error bars
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dance_stats['genre'],
        y=dance_stats['avg_danceability'],
        error_y=dict(
            type='data',
            array=dance_stats['std_danceability'],
            visible=True
        ),
        marker_color='#1DB954',
        name='Rata-rata Danceability'
    ))
    
    fig.update_layout(
        title="Rata-rata Danceability per Genre (dengan Standar Deviasi)",
        xaxis_title="Genre",
        yaxis_title="Danceability",
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Hubungan danceability dengan popularitas
    st.subheader("Hubungan antara Danceability dan Popularitas")
    
    # Scatter plot danceability vs popularitas
    fig = px.scatter(
        df,
        x="danceability",
        y="track_popularity",
        color="playlist_genre",
        hover_name="track_name",
        hover_data=["track_artist"],
        opacity=0.7,
        title="Danceability vs Popularitas Lagu",
        labels={
            "danceability": "Danceability",
            "track_popularity": "Popularitas",
            "playlist_genre": "Genre",
            "track_artist": "Artis",
            "track_name": "Judul Lagu"
        }
    )
    
    # Tambahkan trend line
    fig.update_traces(marker=dict(size=8))
    
    # Tambahkan garis regresi
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan hubungan
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Insight tentang Danceability</h4>
        <p style="color: #FFFFFF;">
            Dari visualisasi di atas, kita dapat mengamati beberapa hal menarik:
            <ul>
                <li>Genre EDM, Pop, dan Rap umumnya memiliki danceability yang lebih tinggi</li>
                <li>Ada korelasi positif tetapi lemah antara danceability dan popularitas</li>
                <li>Lagu-lagu dengan danceability moderat hingga tinggi (0.6-0.8) cenderung lebih populer</li>
                <li>Genre R&B menunjukkan konsistensi danceability yang tinggi (standar deviasi rendah)</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Energy
with tab2:
    st.subheader("Analisis Energy")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #1DB954;">Apa itu Energy?</h4>
            <p style="color: #FFFFFF;">
                Energy adalah ukuran dari 0.0 hingga 1.0 yang mewakili persepsi intensitas dan aktivitas.
                Biasanya, lagu yang energik terasa cepat, keras, dan bising.
                <br><br>
                Misalnya, death metal memiliki energy tinggi, sedangkan prelude Bach mendapat skor rendah pada skala ini.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter genre
        genres = ["Semua Genre"] + sorted(df['playlist_genre'].unique().tolist())
        selected_genre = st.selectbox("Filter Genre", genres, key="energy_genre")
        
        # Tambahkan informasi tambahan
        spotify_card(
            "Fitur Perseptual",
            "Fitur yang berkontribusi pada atribut energy meliputi dynamic range, loudness, timbre, tingkat onset, dan entropi secara umum.",
            "⚡"
        )
    
    with col2:
        # Filter data berdasarkan genre
        if selected_genre != "Semua Genre":
            genre_df = df[df['playlist_genre'] == selected_genre]
        else:
            genre_df = df
        
        # Histogram energy
        fig = px.histogram(
            genre_df,
            x="energy",
            color="playlist_genre" if selected_genre == "Semua Genre" else None,
            nbins=30,
            opacity=0.7,
            title="Distribusi Energy" + (f" - {selected_genre}" if selected_genre != "Semua Genre" else ""),
            labels={"energy": "Energy", "count": "Jumlah Lagu"}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Hubungan energy dengan loudness
    st.subheader("Hubungan antara Energy dan Loudness")
    
    # Scatter plot energy vs loudness dengan regresi
    fig = px.scatter(
        df,
        x="energy",
        y="loudness",
        color="playlist_genre",
        hover_name="track_name",
        hover_data=["track_artist"],
        opacity=0.7,
        trendline="ols",
        title="Energy vs Loudness (Kekuatan Suara)",
        labels={
            "energy": "Energy",
            "loudness": "Loudness (dB)",
            "playlist_genre": "Genre",
            "track_artist": "Artis",
            "track_name": "Judul Lagu"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan hubungan
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Insight tentang Energy dan Loudness</h4>
        <p style="color: #FFFFFF;">
            Terdapat korelasi yang sangat kuat antara energy dan loudness (kenyaringan) lagu:
            <ul>
                <li>Semakin tinggi energy lagu, semakin keras (loudness tinggi) lagu tersebut</li>
                <li>Korelasi ini konsisten di berbagai genre musik</li>
                <li>Hal ini menunjukkan bahwa loudness adalah komponen utama dari persepsi energy dalam musik</li>
                <li>Genre seperti Rock dan EDM menunjukkan kombinasi energy dan loudness yang tinggi</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 3: Valence
with tab3:
    st.subheader("Analisis Valence (Mood/Suasana Musik)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #1DB954;">Apa itu Valence?</h4>
            <p style="color: #FFFFFF;">
                Valence adalah ukuran dari 0.0 hingga 1.0 yang menggambarkan positivitas musik.
                <br><br>
                <strong>Valence Tinggi (0.7-1.0):</strong> Lagu terdengar lebih positif (senang, ceria, euforia)<br>
                <strong>Valence Rendah (0.0-0.3):</strong> Lagu terdengar lebih negatif (sedih, depresi, marah)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter genre
        genres = ["Semua Genre"] + sorted(df['playlist_genre'].unique().tolist())
        selected_genre = st.selectbox("Filter Genre", genres, key="valence_genre")
        
        # Tambahkan opsi untuk melihat valence vs energy
        show_energy = st.checkbox("Tampilkan hubungan dengan Energy", value=True)
    
    with col2:
        # Filter data berdasarkan genre
        if selected_genre != "Semua Genre":
            genre_df = df[df['playlist_genre'] == selected_genre]
        else:
            genre_df = df
        
        # Histogram valence
        fig = px.histogram(
            genre_df,
            x="valence",
            color="playlist_genre" if selected_genre == "Semua Genre" else None,
            nbins=30,
            opacity=0.7,
            title="Distribusi Valence (Mood)" + (f" - {selected_genre}" if selected_genre != "Semua Genre" else ""),
            labels={"valence": "Valence", "count": "Jumlah Lagu"}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Valence vs Energy (Mood Matrix)
    if show_energy:
        st.subheader("Mood Matrix: Valence vs Energy")
        
        # Scatter plot valence vs energy
        fig = px.scatter(
            df,
            x="valence",
            y="energy",
            color="playlist_genre",
            hover_name="track_name",
            hover_data=["track_artist"],
            opacity=0.7,
            title="Mood Matrix (Valence vs Energy)",
            labels={
                "valence": "Valence (Positivity)",
                "energy": "Energy",
                "playlist_genre": "Genre"
            }
        )
        
        # Tambahkan anotasi untuk kuadran
        fig.add_annotation(x=0.25, y=0.75, text="Angry/Tense", showarrow=False, font=dict(color="#E51D2A"))
        fig.add_annotation(x=0.75, y=0.75, text="Happy/Excited", showarrow=False, font=dict(color="#1DB954"))
        fig.add_annotation(x=0.25, y=0.25, text="Sad/Depressing", showarrow=False, font=dict(color="#B3B3B3"))
        fig.add_annotation(x=0.75, y=0.25, text="Chill/Peaceful", showarrow=False, font=dict(color="#4688F2"))
        
        # Tambahkan garis untuk kuadran
        fig.add_shape(type="line", x0=0.5, y0=0, x1=0.5, y1=1, line=dict(color="White", width=1, dash="dash"))
        fig.add_shape(type="line", x0=0, y0=0.5, x1=1, y1=0.5, line=dict(color="White", width=1, dash="dash"))
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Penjelasan Mood Matrix
        st.markdown("""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
            <h4 style="color: #1DB954;">Memahami Mood Matrix</h4>
            <p style="color: #FFFFFF;">
                Mood Matrix menggabungkan valence (positivitas) dan energy untuk mengkategorikan lagu berdasarkan mood/suasana:
                <ul>
                    <li><strong>Happy/Excited (Valence Tinggi, Energy Tinggi):</strong> Lagu yang ceria, semangat, euforia</li>
                    <li><strong>Chill/Peaceful (Valence Tinggi, Energy Rendah):</strong> Lagu yang menenangkan, damai, santai</li>
                    <li><strong>Angry/Tense (Valence Rendah, Energy Tinggi):</strong> Lagu yang intens, agresif, tegang</li>
                    <li><strong>Sad/Depressing (Valence Rendah, Energy Rendah):</strong> Lagu yang sedih, melankolis, depresi</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Rata-rata valence per genre
    st.subheader("Mood Musik per Genre")
    
    # Menghitung rata-rata valence per genre
    valence_avg = df.groupby('playlist_genre')['valence'].mean().sort_values()
    
    # Bar chart untuk rata-rata valence
    fig = px.bar(
        x=valence_avg.values,
        y=valence_avg.index,
        orientation='h',
        color=valence_avg.values,
        color_continuous_scale='RdYlGn',  # Red to Green scale for mood
        title="Rata-rata Valence (Mood) per Genre",
        labels={
            "x": "Valence",
            "y": "Genre",
            "color": "Valence"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan valence per genre
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Insight tentang Mood Musik di Berbagai Genre</h4>
        <p style="color: #FFFFFF;">
            Graf di atas menunjukkan mood rata-rata (valence) dari berbagai genre musik:
            <ul>
                <li>Genre seperti Latin dan Pop cenderung memiliki mood yang lebih positif (valence tinggi)</li>
                <li>Rock dan R&B memiliki valence menengah, menunjukkan keseimbangan lagu positif dan negatif</li>
                <li>Genre tertentu cenderung memiliki mood yang lebih gelap atau sedih (valence rendah)</li>
                <li>Valence tidak berkorelasi langsung dengan popularitas - setiap mood memiliki penggemarnya masing-masing</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 4: Tempo & Duration
with tab4:
    st.subheader("Analisis Tempo dan Durasi Lagu")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #1DB954;">Apa itu Tempo?</h4>
            <p style="color: #FFFFFF;">
                Tempo adalah estimasi kecepatan atau pace dari sebuah lagu dalam beat per minute (BPM).
                <br><br>
                Dalam terminologi musik, tempo adalah kecepatan atau pace dari sebuah lagu dan berasal langsung dari durasi beat rata-rata.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter genre
        genres = ["Semua Genre"] + sorted(df['playlist_genre'].unique().tolist())
        selected_genre = st.selectbox("Filter Genre", genres, key="tempo_genre")
        
        # Informasi tambahan
        spotify_card(
            "Durasi",
            "Durasi lagu diukur dalam milidetik. Rata-rata lagu pop modern berdurasi sekitar 3-4 menit (180.000-240.000 ms).",
            "⏱️"
        )
    
    with col2:
        # Filter data berdasarkan genre
        if selected_genre != "Semua Genre":
            genre_df = df[df['playlist_genre'] == selected_genre]
        else:
            genre_df = df
        
        # Histogram tempo
        fig = px.histogram(
            genre_df,
            x="tempo",
            color="playlist_genre" if selected_genre == "Semua Genre" else None,
            nbins=30,
            opacity=0.7,
            title="Distribusi Tempo" + (f" - {selected_genre}" if selected_genre != "Semua Genre" else ""),
            labels={"tempo": "Tempo (BPM)", "count": "Jumlah Lagu"}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(40,40,40,0.8)',
            paper_bgcolor='rgba(40,40,40,0.8)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Rata-rata tempo per genre
    st.subheader("Perbandingan Tempo antar Genre")
    
    # Menghitung rata-rata tempo per genre
    tempo_avg = df.groupby('playlist_genre')['tempo'].mean().sort_values()
    tempo_std = df.groupby('playlist_genre')['tempo'].std()
    
    # Membuat dataframe untuk plotting
    tempo_stats = pd.DataFrame({
        'genre': tempo_avg.index,
        'avg_tempo': tempo_avg.values,
        'std_tempo': tempo_std.values
    })
    
    # Plot tempo dengan error bars
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tempo_stats['genre'],
        y=tempo_stats['avg_tempo'],
        error_y=dict(
            type='data',
            array=tempo_stats['std_tempo'],
            visible=True
        ),
        marker_color='#1DB954',
        name='Rata-rata Tempo'
    ))
    
    fig.update_layout(
        title="Rata-rata Tempo per Genre (dengan Standar Deviasi)",
        xaxis_title="Genre",
        yaxis_title="Tempo (BPM)",
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Durasi lagu
    st.subheader("Analisis Durasi Lagu")
    
    # Konversi durasi ke menit untuk visualisasi
    df['duration_min'] = df['duration_ms'] / 60000
    
    # Box plot durasi per genre
    fig = px.box(
        df,
        x="playlist_genre",
        y="duration_min",
        color="playlist_genre",
        title="Distribusi Durasi Lagu per Genre",
        labels={
            "duration_min": "Durasi (menit)",
            "playlist_genre": "Genre"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Penjelasan tempo dan durasi
    st.markdown("""
    <div style="background-color: #282828; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1DB954;">Insight tentang Tempo dan Durasi</h4>
        <p style="color: #FFFFFF;">
            Dari visualisasi di atas, kita dapat mengamati:
            <ul>
                <li>EDM dan Pop cenderung memiliki tempo yang lebih cepat</li>
                <li>Rock memiliki standar deviasi tempo yang tinggi, menunjukkan keberagaman tempo dalam genre ini</li>
                <li>Lagu-lagu EDM umumnya lebih panjang durasinya, mungkin karena termasuk extended mixes</li>
                <li>Pop cenderung memiliki durasi yang lebih konsisten, menunjukkan format radio-friendly</li>
                <li>Outlier pada box plot menunjukkan lagu-lagu dengan durasi yang sangat panjang atau sangat pendek</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scatter plot tempo vs durasi
    st.subheader("Hubungan Tempo dengan Durasi")
    
    fig = px.scatter(
        df,
        x="tempo",
        y="duration_min",
        color="playlist_genre",
        size="track_popularity",
        hover_name="track_name",
        hover_data=["track_artist"],
        opacity=0.7,
        title="Tempo vs Durasi Lagu",
        labels={
            "tempo": "Tempo (BPM)",
            "duration_min": "Durasi (menit)",
            "playlist_genre": "Genre",
            "track_popularity": "Popularitas"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(40,40,40,0.8)',
        paper_bgcolor='rgba(40,40,40,0.8)',
        font_color='white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
display_footer() 
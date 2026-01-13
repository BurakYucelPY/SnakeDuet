"""
SnakeDuet - Oyun Sayfası
WebRTC ile gerçek zamanlı oyun
"""
import streamlit as st
import sys
from pathlib import Path

# Utils modülünü import et
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import apply_common_styles, render_footer

# Streamlit WebRTC
from streamlit_webrtc import webrtc_streamer

# Processor import
sys.path.insert(0, str(Path(__file__).parent.parent))
from processor import VideoIsleyici

# Sayfa ayarları
st.set_page_config(
    page_title="Oyun | SnakeDuet",
    page_icon=":material/sports_esports:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Oyun sayfası özel stilleri
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Sidebar gizle */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* WebRTC video büyük göster */
    .stVideo, video {
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
    }
    
    /* WebRTC seçim kutularını gizle */
    [data-testid="stSelectbox"],
    .stSelectbox,
    div[data-baseweb="select"] {
        display: none !important;
    }
    
    /* Oyun konteyner */
    .game-container {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.2);
    }
    
    /* Skor tablosu */
    .score-board {
        display: flex;
        justify-content: space-around;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.9);
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .score-item {
        text-align: center;
    }
    
    .score-label {
        font-size: 0.9rem;
        color: #888;
    }
    
    .score-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Buton stilleri */
    .stButton > button {
        padding: 0.8rem 2rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .red-btn > button {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(255, 68, 68, 0.4);
    }
    
    .red-btn > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 68, 68, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# Üst bar - Geri butonu ve başlık
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown('<div class="red-btn">', unsafe_allow_html=True)
    if st.button("← ÇIKIŞ", key="exit"):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <h1 style="text-align: center; color: #00ff00; font-family: 'Courier New', monospace; margin: 0;">
        SnakeDuet
    </h1>
    <p style="text-align: center; color: #888; margin: 0;">
        Ellerini göster ve oynamaya başla!
    </p>
    """, unsafe_allow_html=True)

with col3:
    pass

st.markdown("<br>", unsafe_allow_html=True)

# Oyun alanı
st.markdown("""
<div style="text-align: center;">
    <div style="display: inline-flex; gap: 2rem; justify-content: center; margin-bottom: 1rem;">
        <div style="background: rgba(0,255,0,0.2); padding: 0.5rem 1.5rem; border-radius: 10px; border: 1px solid #00ff00;">
            <span style="color: #00ff00; font-weight: bold;">YESIL YILAN</span>
            <span style="color: #888;"> - Sol El</span>
        </div>
        <div style="background: rgba(255,0,0,0.2); padding: 0.5rem 1.5rem; border-radius: 10px; border: 1px solid #ff4444;">
            <span style="color: #ff4444; font-weight: bold;">KIRMIZI YILAN</span>
            <span style="color: #888;"> - Sag El</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# WebRTC Oyun Alanı
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # WebRTC Stream
    webrtc_ctx = webrtc_streamer(
        key="snakeduet-game",
        video_processor_factory=VideoIsleyici,
        rtc_configuration={
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},
                {"urls": ["stun:stun1.l.google.com:19302"]},
                {"urls": ["stun:stun2.l.google.com:19302"]},
            ]
        },
        media_stream_constraints={
            "video": {
                "width": {"ideal": 1280},
                "height": {"ideal": 720}
            },
            "audio": False
        },
        async_processing=True,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Alt bilgi
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(0,0,0,0.5); border-radius: 10px;">
        <span style="font-size: 1.5rem;">☝️ ↑</span>
        <p style="color: #888; margin: 0;">Yukarı</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(0,0,0,0.5); border-radius: 10px;">
        <span style="font-size: 1.5rem;">👈 ← | → 👉</span>
        <p style="color: #888; margin: 0;">Sol / Sağ</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(0,0,0,0.5); border-radius: 10px;">
        <span style="font-size: 1.5rem;">👇 ↓</span>
        <p style="color: #888; margin: 0;">Aşağı</p>
    </div>
    """, unsafe_allow_html=True)

# Oyun durumu bilgisi
if webrtc_ctx.state.playing:
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <p style="color: #00ff00; font-size: 1.2rem;">
            🟢 Oyun Aktif - Ellerini Göster!
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <p style="color: #ffcc00; font-size: 1.2rem;">
            ⚠️ Kamerayı başlatmak için "START" butonuna tıkla
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
render_footer()

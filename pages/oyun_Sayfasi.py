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
        background: #0a0a0a;
    }
    
    /* Üst padding kaldır */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Sidebar gizle */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* WebRTC video çok büyük göster */
    video {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        min-height: 70vh !important;
        border-radius: 10px;
        object-fit: contain;
    }
    
    /* WebRTC container büyüt */
    .stVideo {
        width: 100% !important;
    }
    
    /* iframe varsa onu da büyüt */
    iframe {
        width: 100% !important;
        min-height: 70vh !important;
    }
    
    /* START butonu büyüt */
    [data-testid="stWebRtcStreamer"] button,
    .stWebRtcComponent button {
        padding: 1rem 3rem !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 10px !important;
        cursor: pointer !important;
    }
    
    /* SELECT DEVICE gizle */
    [data-testid="stSelectbox"],
    .stSelectbox,
    div[data-baseweb="select"] {
        display: none !important;
    }
    
    /* Oyun konteyner */
    .game-container {
        background: rgba(0, 0, 0, 0.9);
        border: 3px solid #00ff00;
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 0 50px rgba(0, 255, 0, 0.3);
        width: 100%;
    }
    
    /* Buton stilleri */
    .red-btn > button {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
        color: #ffffff !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Üst bar - sadece çıkış butonu
col1, col2 = st.columns([1, 10])

with col1:
    st.markdown('<div class="red-btn">', unsafe_allow_html=True)
    if st.button("← ÇIKIŞ", key="exit"):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# WebRTC Oyun Alanı - tam genişlik
st.markdown('<div class="game-container">', unsafe_allow_html=True)

webrtc_ctx = webrtc_streamer(
    key="snakeduet-game",
    video_processor_factory=VideoIsleyici,
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
        ]
    },
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1920},
            "height": {"ideal": 1080}
        },
        "audio": False
    },
    async_processing=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# Oyun durumu bilgisi
if not webrtc_ctx.state.playing:
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <p style="color: #ffcc00; font-size: 1.1rem;">
            Kamerayı başlatmak için "START" butonuna tıkla
        </p>
    </div>
    """, unsafe_allow_html=True)

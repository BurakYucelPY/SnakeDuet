import streamlit as st
from streamlit_webrtc import webrtc_streamer
from processor import VideoIsleyici

st.set_page_config(page_title="SnakeDuet", layout="wide")

# Session state ile oyun durumunu kontrol et
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False

# CSS ile özelleştirme
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .block-container {
        padding-top: 3rem !important;
    }
    /* Tüm içeriği ortala */
    [data-testid="stVerticalBlock"] {
        align-items: center;
    }
    /* Webrtc kontrollerini tamamen gizle */
    [data-testid="stSelectbox"], 
    .stSelectbox,
    div[data-baseweb="select"],
    .css-1inwz65,
    .css-16idsys p {
        display: none !important;
    }
    /* START butonunu stillendir */
    .stButton > button {
        background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        padding: 20px 80px !important;
        font-size: 24px !important;
        border-radius: 15px !important;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5) !important;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00ff00; font-family: Courier New; font-size: 48px; text-shadow: 2px 2px 4px #000;'>🐍 SnakeDuet 🐍</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 20px;'>Ellerinle Yılanları Yönet!</p>", unsafe_allow_html=True)

if not st.session_state.oyun_basladi:
    # Başlangıç ekranı - sadece START butonu
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("▶  START"):
            st.session_state.oyun_basladi = True
            st.rerun()
else:
    # Oyun başladı - webrtc göster
    webrtc_streamer(
        key="hareket-fix",
        video_processor_factory=VideoIsleyici,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
    )
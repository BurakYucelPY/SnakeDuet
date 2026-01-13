"""
SnakeDuet - Ana Sayfa
El hareketleriyle kontrol edilen çift yılanlı oyun
"""
import streamlit as st
import sys
from pathlib import Path

# Utils modülünü import et
sys.path.insert(0, str(Path(__file__).parent))
from utils.styles import (
    set_background_image, 
    apply_common_styles, 
    render_header,
    render_footer
)

# Sayfa ayarları
st.set_page_config(
    page_title="SnakeDuet",
    page_icon=":material/sports_esports:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Arkaplan görselini ayarla
ASSETS_PATH = Path(__file__).parent / "assets"
BACKGROUND_IMAGE = ASSETS_PATH / "foto.png"

if BACKGROUND_IMAGE.exists():
    set_background_image(str(BACKGROUND_IMAGE))

# Ortak stilleri uygula
apply_common_styles()

# Başlığı render et
render_header()

# Ana içerik
st.markdown("<br>", unsafe_allow_html=True)

# Merkezi buton düzeni
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Oyunu Başlat Butonu
    st.markdown('<div class="green-btn">', unsafe_allow_html=True)
    if st.button("OYUNU BASLAT", key="start_game", use_container_width=True):
        st.switch_page("pages/oyun_Sayfasi.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Nasıl Oynanır Butonu
    st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
    if st.button("NASIL OYNANIR?", key="how_to_play", use_container_width=True):
        st.switch_page("pages/nasil_Oynanir.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
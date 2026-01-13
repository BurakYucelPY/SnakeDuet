"""
SnakeDuet - Nasıl Oynanır?
Oyun kuralları ve talimatlar
"""
import streamlit as st
import sys
from pathlib import Path

# Utils modülünü import et
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import (
    apply_common_styles,
    render_footer
)

# Sayfa ayarları
st.set_page_config(
    page_title="Nasil Oynanir | SnakeDuet",
    page_icon=":material/sports_esports:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Koyu arkaplan stili
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
    }
</style>
""", unsafe_allow_html=True)

# Ortak stilleri uygula
apply_common_styles()

# Geri butonu
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.markdown('<div class="red-btn">', unsafe_allow_html=True)
    if st.button("← GERİ", key="back"):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Başlık
st.markdown("""
<div style="text-align: center; padding: 0.5rem 0;">
    <h1 style="color: #00ff00; font-size: 2.5rem; font-family: 'Courier New', monospace;">
        Nasil Oynanir?
    </h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# İçerik kartları
col1, col2 = st.columns(2)

with col1:
    # Kontroller
    st.markdown("""
    <div class="content-box">
        <h2 style="color: #00ff00; text-align: center;">🎮 Kontroller</h2>
        <br>
        <div style="padding: 0.5rem;">
            <p style="color: #ffffff; font-size: 1.1rem;">
                <strong style="color: #00ff00;">Sol El</strong> → Yeşil Yılanı Kontrol Eder
            </p>
            <p style="color: #ffffff; font-size: 1.1rem;">
                <strong style="color: #ff4444;">Sağ El</strong> → Kırmızı Yılanı Kontrol Eder
            </p>
        </div>
        <br>
        <h3 style="color: #ffcc00; text-align: center;">Yön Hareketleri</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 1rem;">
            <div style="text-align: center; background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 10px;">
                <span style="font-size: 2rem;">☝️</span>
                <p style="color: #00ff00; margin: 0;">YUKARI</p>
                <small style="color: #888;">Parmak yukarı</small>
            </div>
            <div style="text-align: center; background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 10px;">
                <span style="font-size: 2rem;">👇</span>
                <p style="color: #00ff00; margin: 0;">AŞAĞI</p>
                <small style="color: #888;">Parmak aşağı</small>
            </div>
            <div style="text-align: center; background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 10px;">
                <span style="font-size: 2rem;">👈</span>
                <p style="color: #00ff00; margin: 0;">SOL</p>
                <small style="color: #888;">Parmak sola</small>
            </div>
            <div style="text-align: center; background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 10px;">
                <span style="font-size: 2rem;">👉</span>
                <p style="color: #00ff00; margin: 0;">SAĞ</p>
                <small style="color: #888;">Parmak sağa</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Oyun Kuralları
    st.markdown("""
    <div class="content-box">
        <h2 style="color: #00ff00; text-align: center;">📋 Oyun Kuralları</h2>
        <br>
        <ul style="color: #ffffff; font-size: 1.1rem; line-height: 2;">
            <li>🍎 <strong style="color: #ffcc00;">Yemleri</strong> topla ve büyü!</li>
            <li>🏆 Her yem <strong style="color: #00ff00;">+1 puan</strong> kazandırır</li>
            <li>🚫 Duvarlara <strong style="color: #ff4444;">çarpma</strong> - oyun biter!</li>
            <li>⚠️ Kendi gövdene <strong style="color: #ff4444;">çarpma</strong></li>
            <li>🤝 İki yılanı <strong style="color: #00bfff;">aynı anda</strong> kontrol et</li>
        </ul>
    </div>
    
    <br>
    
    <div class="content-box">
        <h2 style="color: #00ff00; text-align: center;">💡 İpuçları</h2>
        <br>
        <ul style="color: #ffffff; font-size: 1rem; line-height: 2;">
            <li>✨ Ellerini kameranın <strong>net görebileceği</strong> şekilde tut</li>
            <li>💡 <strong>İyi aydınlatma</strong> el takibini iyileştirir</li>
            <li>🎯 <strong>Yavaş ve kontrollü</strong> hareketler yap</li>
            <li>🖐️ Ellerini <strong>ekranın iki yarısında</strong> tut</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Başlat butonu
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="green-btn">', unsafe_allow_html=True)
    if st.button("🎮  OYUNA BAŞLA!", key="start_game", use_container_width=True):
        st.switch_page("pages/oyun_Sayfasi.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()

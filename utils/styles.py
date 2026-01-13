"""
Ortak stil ve yardımcı fonksiyonlar
"""
import base64
import streamlit as st
from pathlib import Path

def get_base64_image(image_path: str) -> str:
    """Görseli base64 formatına çevirir"""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_image(image_path: str):
    """Sayfa arkaplanına görsel ekler"""
    base64_img = get_base64_image(image_path)
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)

def apply_common_styles():
    """Tüm sayfalarda kullanılacak ortak stiller"""
    st.markdown("""
    <style>
    /* Sidebar gizle */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Ana container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Başlık stilleri */
    .game-title {
        font-family: 'Courier New', monospace;
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        color: #00ff00;
        text-shadow: 
            0 0 10px #00ff00,
            0 0 20px #00ff00,
            0 0 30px #00ff00,
            0 0 40px #00ff00;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 
                0 0 10px #00ff00,
                0 0 20px #00ff00,
                0 0 30px #00ff00;
        }
        to {
            text-shadow: 
                0 0 20px #00ff00,
                0 0 30px #00ff00,
                0 0 40px #00ff00,
                0 0 50px #00ff00;
        }
    }
    
    .subtitle {
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.5rem;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Buton stilleri */
    .stButton > button {
        width: 100%;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 15px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Yeşil buton - Ana aksiyon */
    .green-btn > button {
        background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%) !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    }
    
    .green-btn > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.8);
    }
    
    /* Mavi buton - Bilgi */
    .blue-btn > button {
        background: linear-gradient(135deg, #00bfff 0%, #0080ff 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.5);
    }
    
    .blue-btn > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 191, 255, 0.8);
    }
    
    /* Turuncu buton - Ayarlar */
    .orange-btn > button {
        background: linear-gradient(135deg, #ff8c00 0%, #ff6600 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.5);
    }
    
    .orange-btn > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 140, 0, 0.8);
    }
    
    /* Kırmızı buton - Geri */
    .red-btn > button {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(255, 68, 68, 0.5);
    }
    
    .red-btn > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255, 68, 68, 0.8);
    }
    
    /* Kart stilleri */
    .game-card {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }
    
    /* İçerik kutusu */
    .content-box {
        background: rgba(0, 0, 0, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Yılan emojileri animasyonu */
    .snake-emoji {
        font-size: 3rem;
        display: inline-block;
        animation: snake-move 2s ease-in-out infinite;
    }
    
    @keyframes snake-move {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Oyun başlığını render eder"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 class="game-title">SnakeDuet</h1>
        <p class="subtitle">Ellerinle Yılanları Yönet!</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Footer render eder"""
    st.markdown("""
    <div class="footer">
        SnakeDuet © 2026 | El Hareketleriyle Yılan Oyunu
    </div>
    """, unsafe_allow_html=True)
